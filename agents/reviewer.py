def review(state):
    draft = state.get("draft", "")
    context = state.get("context", "")
    model = state["model"]

    if state.get("route") == "retrieval" and context:
        prompt = f"""Review this answer for grounding.
Answer: {draft}
Evidence: {context}
If the answer contains claims not supported by evidence, rewrite it to remove unsupported claims.
Return only the corrected answer."""
        checked = model.invoke(prompt).content
        return {"draft": checked}
    return {}
