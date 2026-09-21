from app.rag.store import search
from app.config import get_settings


def retrieve(state):
    results = search(state["message"], get_settings().top_k)
    context = "\n\n".join(
        f"[{r['chunk_id']}] Source: {r['source']}\n{r['content']}" for r in results
    )
    citations = [{"source": r["source"], "chunk_id": r["chunk_id"]} for r in results]
    return {"context": context, "citations": citations}
