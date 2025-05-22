import os
import json
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from contextlib import AsyncExitStack
from typing import Optional
from application.model.prompt_manager import PromptManager

load_dotenv()  # load environment variables from .env
prompt_manager = PromptManager()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(api_key=os.getenv('API_KEY'))
        command = "python"
        self.server_params = StdioServerParameters(
            command=command,
            args=['application/mcp/server.py'],
            env=None
        )

    async def process_query(self, query: str, history) -> str:
        """Process a query using Gemini and available tools"""

        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:

                # Initialize server
                await session.initialize()
                enhanced_query = prompt_manager.initial_prompt(user_prompt=query)
                
                messages = []
                for msg in history:
                    messages.append(types.Content(role=msg['role'], parts=[types.Part(text=msg['content'])]))
                messages.append(types.Content(role="user", parts=[types.Part(text=enhanced_query)]))

                mcp_tools = await session.list_tools()
                # Remove debug prints
                tools = [
                    types.Tool(
                        function_declarations=[
                            {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": {
                                    k: v
                                    for k, v in tool.inputSchema.items()
                                    if k not in ["additionalProperties", "$schema"]
                                },
                            }
                        ]
                    )
                    for tool in mcp_tools.tools
                ]

                # Initial Gemini API call
                response = self.client.models.generate_content(
                        model="gemini-2.5-flash-preview-05-20",
                        contents=messages,
                        config=types.GenerateContentConfig(
                            temperature=1,
                            top_k=64,
                            top_p=0.95,
                            tools=tools,
                        ),
                    )

                final_text = ""
                final_tuned_text = ""
                check = False

                # Process response and handle tool calls
                if response.text != None:
                    final_text += response.text

                flights = []
                for content in response.candidates[0].content.parts:
                    if hasattr(content, 'function_call') and content.function_call is not None:
                        check = True
                        tool_name = content.function_call.name
                        tool_args = content.function_call.args

                        # Execute tool call
                        result = await session.call_tool(tool_name, tool_args)

                        # Convert assistant message content to proper format
                        assistant_message = types.Content(
                           role="model",
                        parts=[types.Part(text=str(content.text))]
                        )
                        messages.append(assistant_message)

                        flights.append(result.content[0].text)
                        
                if check:
                    # Add user message with tool result
                    user_message = types.Content(
                        role="user",
                        parts=[types.Part(text=prompt_manager.new_second_prompt(flights=flights, initial_user_prompt=query))]
                    )
                    messages.append(user_message)
                            
                    # Get next response from Gemini
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash-preview-05-20",
                        contents=messages,
                        config=types.GenerateContentConfig(
                            temperature=1,
                            top_k=64,                                
                            top_p=0.95,
                            tools=tools,
                        ),
                    )
                    final_tuned_text += response.text   
                    final_text = final_tuned_text

                json_response = {"input": query, "output":final_text}
                json_output = json.dumps(json_response)
                return json_output   