from fastmcp import FastMCP
import os
import importlib
import asyncio # Import asyncio

mcp = FastMCP("MCP Server")

async def register_tools(mcp_instance): # Make it async
    tools_dir = "tools"
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{tools_dir}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, FastMCP):
                    await mcp_instance.import_server(attr, prefix=f"{filename[:-3]}_") # Await the call

# Register tools immediately
asyncio.run(register_tools(mcp))

if __name__ == "__main__":
    mcp.run(transport="http", port=8002)
