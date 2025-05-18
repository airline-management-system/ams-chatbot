from mcp.server.fastmcp import FastMCP
import json
import httpx

# Create server
mcp = FastMCP("ams-chatbot")

"""
TODO:
    - Prompt optimizations can be added
    - Image handlers may be added
    - ...
"""

# Create the tool
#@mcp.tool()
async def get_response(prompt:str) -> str:
    """
    Get response from the LLM model by sending a prompt to the local LLM service.
    
    Args:
        prompt (str): The input prompt to send to the LLM model
        
    Returns:
        str: The response text from the LLM model
        
    Note:
        This function communicates with a local LLM service running on port 8081
    """
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8081/api/v1/generate", headers={"Accept":"application/json", "Content-Type":"application/json"}, data=json.dumps(prompt))
        return response.text

@mcp.tool()
async def send_query_to_service(query:str) -> str:
    """
    Send a GET request to query the database for aviation-related information.
    This function can query various types of information including:
    - Flight details and schedules
    - Aircraft/plane information
    - Other aviation-related data
    
    Args:
        query (str): The complete URL endpoint to query. This should be a valid API endpoint
                    that returns aviation-related data.
        
    Returns:
        str: The response text from the service containing the requested information
        
    Note:
        This function makes a GET request to the specified URL endpoint
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(query, headers={"Accept":"*/*"})
        return response.text

if __name__ == "__main__":
    mcp.run(transport="stdio")