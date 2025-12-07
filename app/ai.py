import asyncio
from fastmcp import Client

# Initialize FastMCP client
mcp_client = Client("http://mcp:8002/mcp")

async def train_and_predict_stock_via_mcp(product_id: int, company_id: int, sales_data: list) -> float:
    """
    Calls the FastMCP server to predict next month's sales based on historical sales data.
    """
    async with mcp_client:
        result = await mcp_client.call_tool(
            "ai_tools_predict_stock",
            {"product_id": product_id, "company_id": company_id, "sales_data": sales_data}
        )
        if "error" in result:
            # Handle error from MCP server
            print(f"Error from MCP server: {result['error']}")
            return 0.0 # Or raise an exception
        return result.get("predicted_stock_next_month", 0.0)
