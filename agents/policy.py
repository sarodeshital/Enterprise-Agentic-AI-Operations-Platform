def policy_analysis(state):
    model = state["model"]
    prompt = f"""You are an enterprise policy analyst.
Answer only from the retrieved context. If the context is insufficient, say so.
Preserve important conditions, exceptions and dates.

USER QUESTION:
{state["message"]}

RETRIEVED CONTEXT:
{state.get("context", "")}
"""
    response = model.invoke(prompt)
    return {"draft": response.content}
