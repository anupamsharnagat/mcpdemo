import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client():
    """
    Connect to the MCP server using Standard I/O and call the 'add_numbers' tool.
    """
    # Define the parameters to launch the server
    # We use 'python server.py --transport stdio' to run the server in stdio mode
    server_params = StdioServerParameters(
        command="python",
        args=["server.py", "--transport", "stdio"],
        env=None
    )

    print("Connecting to MCP server via stdio...")
    
    # Initialize the stdio client
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Create a session with the server
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the session (required)
            await session.initialize()
            print("Session initialized.")

            # List available tools to verify
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

            # Call the 'add_numbers' tool
            print("Calling 'add_numbers' with a=10, b=20...")
            result = await session.call_tool("add_numbers", arguments={"a": 10, "b": 20})
            
            # Print the result
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_client())
