from uuid import uuid4
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from app.graph import run_agent
from app.schemas import ChatRequest, ChatResponse
from app.observability import REQUESTS, Timer
from app.rag.store import init_db

app = FastAPI(title="Enterprise Agentic AI Platform", version="1.0.0")


@app.on_event("startup")
def startup():
    try:
        init_db()
    except Exception:
        # DB can be unavailable during local API-only tests.
        pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    thread_id = request.thread_id or str(uuid4())
    with Timer("chat"):
        result = run_agent(request.message)
    route = result.get("route", "general")
    REQUESTS.labels(route).inc()
    return ChatResponse(
        thread_id=thread_id,
        answer=result.get("answer", ""),
        citations=result.get("citations", []),
        route=route,
        tool_calls=result.get("tool_calls", []),
    )


@app.websocket("/v1/ws/{thread_id}")
async def websocket_chat(websocket: WebSocket, thread_id: str):
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            message = payload.get("message", "")
            if not message:
                await websocket.send_json({"error": "message is required"})
                continue
            result = run_agent(message)
            await websocket.send_json({
                "thread_id": thread_id,
                "answer": result.get("answer", ""),
                "route": result.get("route", "general"),
                "citations": result.get("citations", []),
                "tool_calls": result.get("tool_calls", []),
            })
    except WebSocketDisconnect:
        return
