from app.rag.chunking import split_document


def test_chunking():
    chunks = split_document("A" * 2000)
    assert len(chunks) > 1
    assert all(chunks)
