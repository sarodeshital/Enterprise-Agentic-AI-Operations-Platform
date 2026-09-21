def final_answer(state):
    draft = state.get("draft")
    if draft:
        return {"answer": draft}
    model = state["model"]
    response = model.invoke(state["message"])
    return {"answer": response.content}
