from app.services.tools import create_support_ticket


def action_agent(state):
    message = state["message"]
    # Demo safety rule: actions are represented as a proposed tool call.
    # Add authenticated user identity + explicit authorization before enabling writes.
    if "ticket" in message.lower() or "incident" in message.lower():
        result = create_support_ticket(
            title="AI-created support request",
            description=message,
        )
        return {"draft": result["message"], "tool_calls": ["create_support_ticket"]}
    return {"draft": "I identified an action request, but no approved action tool matched it.", "tool_calls": []}
