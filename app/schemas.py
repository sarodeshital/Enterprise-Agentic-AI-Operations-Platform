from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    thread_id: str | None = None


class Citation(BaseModel):
    source: str
    chunk_id: str


class ChatResponse(BaseModel):
    thread_id: str
    answer: str
    citations: list[Citation] = []
    route: str = "general"
    tool_calls: list[str] = []
