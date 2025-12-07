from fastmcp import FastMCP

tools_server = FastMCP(name="UserManagement")

@tools_server.tool
def greet(name: str) -> str:
    """
    A simple tool to greet a user.
    """
    return f"Hello, {name}!"

@tools_server.tool
def get_user(user_id: int) -> dict:
    """
    Gets user information from a user ID.
    """
    # In a real application, this would fetch user data from a database.
    # Here, we'll just return some dummy data.
    if user_id == 1:
        return {"id": 1, "name": "Alice", "email": "alice@example.com"}
    elif user_id == 2:
        return {"id": 2, "name": "Bob", "email": "bob@example.com"}
    else:
        return {"error": "User not found"}