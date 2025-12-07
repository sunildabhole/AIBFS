import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8002/mcp") # Connect to your FastMCP server

async def main():
    async with client:
        # Call the greet tool
        greet_result = await client.call_tool("user_management_greet", {"name": "Alice"})
        print(f"Greet result: {greet_result}")

        # Call the get_user tool
        user_result = await client.call_tool("user_management_get_user", {"user_id": 1})
        print(f"User result: {user_result}")

        user_not_found_result = await client.call_tool("user_management_get_user", {"user_id": 99})
        print(f"User not found result: {user_not_found_result}")

        # Call the create_order_and_invoice tool
        order_data = {
            "items": [{"product_id": 1, "quantity": 2}],
            "customer_id": 1
        }
        invoice_result = await client.call_tool("billing_create_order_and_invoice", {"order": order_data, "user_id": 1, "company_id": 1})
        print(f"Invoice result: {invoice_result}")

        # Call the report generation tools
        sales_report_json = await client.call_tool("reports_get_sales_report", {"start_date": "2023-01-01", "end_date": "2023-12-31", "company_id": 1, "format": "json"})
        print(f"Sales report (JSON): {sales_report_json}")

        sales_report_pdf = await client.call_tool("reports_get_sales_report", {"start_date": "2023-01-01", "end_date": "2023-12-31", "company_id": 1, "format": "pdf"})
        print(f"Sales report (PDF): {sales_report_pdf}")

        low_stock_report_json = await client.call_tool("reports_get_low_stock_report", {"company_id": 1, "limit": 5, "format": "json"})
        print(f"Low stock report (JSON): {low_stock_report_json}")

        low_stock_report_pdf = await client.call_tool("reports_get_low_stock_report", {"company_id": 1, "limit": 5, "format": "pdf"})
        print(f"Low stock report (PDF): {low_stock_report_pdf}")

        top_selling_report_json = await client.call_tool("reports_get_top_selling_report", {"company_id": 1, "limit": 5, "format": "json"})
        print(f"Top selling report (JSON): {top_selling_report_json}")

        top_selling_report_pdf = await client.call_tool("reports_get_top_selling_report", {"company_id": 1, "limit": 5, "format": "pdf"})
        print(f"Top selling report (PDF): {top_selling_report_pdf}")

        total_revenue_report_json = await client.call_tool("reports_get_total_revenue_report", {"company_id": 1, "format": "json"})
        print(f"Total revenue report (JSON): {total_revenue_report_json}")

        total_revenue_report_pdf = await client.call_tool("reports_get_total_revenue_report", {"company_id": 1, "format": "pdf"})
        print(f"Total revenue report (PDF): {total_revenue_report_pdf}")

if __name__ == "__main__":
    asyncio.run(main())
