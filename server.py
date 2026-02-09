import argparse
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
import uvicorn
import mcp.types as types

# Initialize the MCP Server
app_server = Server("simple-mcp-server")

@app_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    """
    return [
        types.Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"},
                },
                "required": ["a", "b"],
            },
        )
    ]

@app_server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name == "add_numbers":
        if not arguments:
            raise ValueError("Missing arguments")
            
        a = arguments.get("a")
        b = arguments.get("b")

        if a is None or b is None:
            raise ValueError("Missing 'a' or 'b'")

        result = float(a) + float(b)
        return [
            types.TextContent(
                type="text",
                text=str(result),
            )
        ]

    raise ValueError(f"Unknown tool: {name}")

async def run_stdio():
    """Run the server using Standard I/O transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app_server.run(read_stream, write_stream, app_server.create_initialization_options())

def create_starlette_app(transport_type: str):
    """
    Create a Starlette application for SSE or HTTP transport.
    """
    if transport_type == "sse":
        sse = SseServerTransport("/messages")
        
        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
                await app_server.run(read_stream, write_stream, app_server.create_initialization_options())

        return Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages", app=sse.handle_post_message),
            ]
        )
    elif transport_type == "http":
        async def handle_http(request):
            session_id = request.query_params.get("session_id")
            http_transport = StreamableHTTPServerTransport(mcp_session_id=session_id)
            
            # For HTTP, we often need to run the server in the background or per-request
            # The simplified way is to let handle_request handle the ASGI lifecycle.
            # But the server logic (app_server.run) needs to be connected to the transport.
            
            async with http_transport.connect() as (read_stream, write_stream):
                # Start the server logic in a task
                server_task = asyncio.create_task(
                    app_server.run(read_stream, write_stream, app_server.create_initialization_options())
                )
                try:
                    return await http_transport.handle_request(request.scope, request.receive, request._send)
                finally:
                    # Clean up
                    if not server_task.done():
                        server_task.cancel()
                
        return Starlette(
            routes=[
                Route("/mcp", endpoint=handle_http, methods=["POST", "GET"]),
            ]
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "http"], default="stdio", help="Transport mechanism")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE/HTTP")
    args = parser.parse_args()

    if args.transport == "stdio":
        # Note: Do NOT print to stdout here as it interferes with the MCP stdio transport
        asyncio.run(run_stdio())
    else:
        print(f"Starting MCP server on {args.transport} at http://localhost:{args.port}", flush=True)
        app = create_starlette_app(args.transport)
        uvicorn.run(app, host="0.0.0.0", port=args.port)
