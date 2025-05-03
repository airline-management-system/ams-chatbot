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
@mcp.tool()
async def get_response(prompt:str) -> str:
    """Get response from LLM model"""
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8081/api/v1/generate", headers={"Accept":"application/json", "Content-Type":"application/json"}, data=json.dumps(prompt))
        return response.text


if __name__ == "__main__":
    mcp.run(transport="stdio")