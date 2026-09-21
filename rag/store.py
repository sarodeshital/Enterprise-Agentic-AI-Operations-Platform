from sqlalchemy import create_engine, text
from app.config import get_settings
from app.rag.embeddings import embed_query

engine = create_engine(get_settings().database_url, pool_pre_ping=True)


def init_db():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id BIGSERIAL PRIMARY KEY,
                source TEXT NOT NULL,
                chunk_id TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                embedding vector(1536)
            )
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx
            ON documents USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """))


def upsert_chunks(rows: list[tuple[str, str, str, list[float]]]):
    init_db()
    with engine.begin() as conn:
        for source, chunk_id, content, embedding in rows:
            conn.execute(
                text("""
                INSERT INTO documents(source, chunk_id, content, embedding)
                VALUES (:source, :chunk_id, :content, CAST(:embedding AS vector))
                ON CONFLICT (chunk_id) DO UPDATE SET
                    source = EXCLUDED.source,
                    content = EXCLUDED.content,
                    embedding = EXCLUDED.embedding
                """),
                {
                    "source": source,
                    "chunk_id": chunk_id,
                    "content": content,
                    "embedding": str(embedding),
                },
            )


def search(query: str, k: int = 5):
    init_db()
    vector = str(embed_query(query))
    with engine.begin() as conn:
        result = conn.execute(
            text("""
            SELECT source, chunk_id, content,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS score
            FROM documents
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :k
            """),
            {"embedding": vector, "k": k},
        )
        return [dict(row._mapping) for row in result]
