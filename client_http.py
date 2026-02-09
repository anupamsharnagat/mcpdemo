import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def run_client():
    """
    Connect to the MCP server using Streamable HTTP and call the 'add_numbers' tool.
    Assumes the server is running at http://localhost:8000/mcp
    """
    url = "http://localhost:8000/mcp"
    print(f"Connecting to MCP server via Streamable HTTP at {url}...")
    
    # Initialize the Streamable HTTP client
    # streamable_http_client returns (read_stream, write_stream, get_session_id)
    async with streamable_http_client(url) as (read_stream, write_stream, get_session_id):
        # Create a session with the server
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session (required)
            await session.initialize()
            print("Session initialized.")

            # Call the 'add_numbers' tool
            print("Calling 'add_numbers' with a=100, b=200...")
            result = await session.call_tool("add_numbers", arguments={"a": 100, "b": 200})
            
            # Print the result
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    # Note: Make sure the server is running with --transport http before running this
    asyncio.run(run_client())
