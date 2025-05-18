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

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(api_key=os.getenv('API_KEY'))

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        if not (is_python):
            raise ValueError("Server script must be a .py or .js file")

        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))


        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str, history) -> str:
        """Process a query using Gemini and available tools"""
        await self.connect_to_server('application/mcp/server.py')
        prompt_manager = PromptManager()
        enhanced_query = prompt_manager.initial_prompt(user_prompt=query)
        
        messages = history
        messages.append([
            {
                "role": "user",
                "content": enhanced_query
            }
        ])

        mcp_tools = await self.session.list_tools()
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
                model="gemini-2.0-flash",
                contents=enhanced_query,
                config=types.GenerateContentConfig(
                    tools=tools,
                    response_modalities=['TEXT'],
                ),
            )

        
        # Process response and handle tool calls
        final_text = response.text

        assistant_message_content = []
        for content in response.candidates[0].content.parts:
            if hasattr(content, 'function_call') and content.function_call is not None:
                tool_name = content.function_call.name
                tool_args = content.function_call.args

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                #final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                    "role": "bot",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "content": prompt_manager.enhanced_prompt(user_prompt=result.content[0].text)
                        }
                    ]
                })

                new_prompt = prompt_manager.enhanced_prompt(user_prompt=result.content[0].text)
                # Get next response from Gemini
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        temperature=1,
                        top_k=64,
                        top_p=0.95,
                        tools=tools,
                        response_modalities=['TEXT']
                    ),
                )

                final_text += response.text
                
        json_response = {"input": query, "output":final_text}
        json_output = json.dumps(json_response)
        return json_output   