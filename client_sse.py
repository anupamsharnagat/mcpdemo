import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run_client():
    """
    Connect to the MCP server using SSE and call the 'add_numbers' tool.
    Assumes the server is running at http://localhost:8000/sse
    """
    url = "http://localhost:8000/sse"
    print(f"Connecting to MCP server via SSE at {url}...")
    
    # Initialize the SSE client
    async with sse_client(url) as (read_stream, write_stream):
        # Create a session with the server
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session (required)
            await session.initialize()
            print("Session initialized.")

            # Call the 'add_numbers' tool
            print("Calling 'add_numbers' with a=15, b=25...")
            result = await session.call_tool("add_numbers", arguments={"a": 15, "b": 25})
            
            # Print the result
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    # Note: Make sure the server is running with --transport sse before running this
    asyncio.run(run_client())
