from mcp.server.fastmcp import FastMCP
from app.rag.store import search
from app.services.tools import create_support_ticket, get_employee_profile

mcp = FastMCP("enterprise-agentic-tools")


@mcp.tool()
def search_policy(query: str) -> list[dict]:
    """Search approved enterprise policy documents."""
    return search(query, 5)


@mcp.tool()
def create_ticket(title: str, description: str) -> dict:
    """Create a support ticket. Protect this tool with enterprise authorization in production."""
    return create_support_ticket(title, description)


@mcp.tool()
def employee_profile(employee_id: str) -> dict:
    """Fetch a limited employee profile from an enterprise system."""
    return get_employee_profile(employee_id)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
