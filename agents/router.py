from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Route(BaseModel):
    route: Literal["retrieval", "action", "general"] = Field(
        description="retrieval for enterprise knowledge, action for system changes, general otherwise"
    )


def route_request(state):
    model = state["model"].with_structured_output(Route)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Classify the user request. Use retrieval for questions needing enterprise documents. Use action for requests to perform an enterprise operation. Use general for normal conversation."),
        ("human", "{message}"),
    ])
    route = (prompt | model).invoke({"message": state["message"]})
    return {"route": route.route}
