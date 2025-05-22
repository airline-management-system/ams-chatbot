from mcp.server.fastmcp import FastMCP
import json
import httpx

# Create server
mcp = FastMCP("ams-chatbot")


@mcp.tool()
async def search_flights(http_url:str) -> str:
    """
    Query aviation-related information from external APIs through HTTP GET requests.
    
    This function serves as a generic HTTP client to fetch aviation data from various endpoints.
    It can be used to retrieve:
    - Flight schedules and status
    - Aircraft specifications and details
    - Any other aviation-related data available through HTTP APIs
    
    Args:
        http_url (str): The complete URL endpoint to query. Must be a valid HTTP URL
                       that returns aviation-related data in a supported format (JSON, XML, etc.)
        
    Returns:
        str: The raw response text from the API endpoint containing the requested information
        
    Raises:
        httpx.HTTPError: If the HTTP request fails (e.g., network error, invalid URL)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url=http_url, headers={"Accept":"*/*"})
        return response.text
    
@mcp.tool()
async def search_return_flights(http_url:str) -> str:
    """
    Query return flight information from external APIs through HTTP GET requests.
    
    This function specifically handles return flight searches, allowing users to find:
    - Return flight schedules and availability
    - Round-trip flight options
    - Return flight pricing and details
    
    Args:
        http_url (str): The complete URL endpoint to query. Must be a valid HTTP URL
                       that returns return flight data in a supported format (JSON, XML, etc.)
        
    Returns:
        str: The raw response text from the API endpoint containing the return flight information
        
    Raises:
        httpx.HTTPError: If the HTTP request fails (e.g., network error, invalid URL)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url=http_url, headers={"Accept":"*/*"})
        return response.text

if __name__ == "__main__":
    mcp.run(transport="stdio")