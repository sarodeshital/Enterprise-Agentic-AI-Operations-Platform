from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from app.llm import get_chat_model
from app.agents.router import route_request
from app.agents.retrieval import retrieve
from app.agents.policy import policy_analysis
from app.agents.action import action_agent
from app.agents.reviewer import review
from app.agents.final import final_answer


class AgentState(TypedDict, total=False):
    message: str
    model: Any
    route: str
    context: str
    citations: list[dict]
    draft: str
    answer: str
    tool_calls: list[str]


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("router", route_request)
    graph.add_node("retrieve", retrieve)
    graph.add_node("policy", policy_analysis)
    graph.add_node("action", action_agent)
    graph.add_node("review", review)
    graph.add_node("final", final_answer)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        lambda s: s["route"],
        {
            "retrieval": "retrieve",
            "action": "action",
            "general": "final",
        },
    )
    graph.add_edge("retrieve", "policy")
    graph.add_edge("policy", "review")
    graph.add_edge("action", "review")
    graph.add_edge("review", "final")
    graph.add_edge("final", END)
    return graph.compile()


def run_agent(message: str):
    app = build_graph()
    result = app.invoke({
        "message": message,
        "model": get_chat_model(),
        "tool_calls": [],
        "citations": [],
    })
    return result
