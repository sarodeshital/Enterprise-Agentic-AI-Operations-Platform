from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import get_settings


def split_document(text: str):
    s = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=s.chunk_size,
        chunk_overlap=s.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)
