from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

# LangChain imports (v0.3+ split packages)
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


class UploadResponse(BaseModel):
    file_name: str
    chunks: int
    status: str


router = APIRouter()


# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"
VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"


def _ensure_dirs() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)


def _save_upload(file: UploadFile) -> Path:
    """Persist the uploaded file to disk and return its path."""
    _ensure_dirs()
    safe_name = os.path.basename(file.filename or "document")
    dest = UPLOAD_DIR / safe_name
    # If exists, append a counter
    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        i = 1
        while True:
            candidate = dest.with_name(f"{stem}_{i}{suffix}")
            if not candidate.exists():
                dest = candidate
                break
            i += 1
    with dest.open("wb") as f:
        f.write(file.file.read())
    return dest


def _load_documents(path: Path):
    """Load documents from the saved file using appropriate loader."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()
    elif ext in {".txt", ".md"}:
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()
    else:
        raise HTTPException(status_code=415, detail="Unsupported file type. Use PDF or text.")
    # Inject source metadata
    for d in docs:
        d.metadata = {**(d.metadata or {}), "source": str(path.name)}
    return docs


def _split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    return splitter.split_documents(documents)


def _persist_chunks(chunks: list, collection_name: str = "ask_my_docs") -> None:
    # Initialize embeddings and Chroma store (persisted)
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    store = Chroma(
        embedding_function=embeddings,
        collection_name=collection_name,
        persist_directory=str(VECTOR_DIR),
    )
    # Create deterministic IDs to avoid duplicates on repeated uploads
    ids = []
    for i, doc in enumerate(chunks):
        src = doc.metadata.get("source", "doc")
        page = doc.metadata.get("page", 0)
        ids.append(f"{src}::p{page}::i{i}")
        
    store.add_documents(chunks, ids=ids)
    # Explicit persist (Chroma persists automatically, but we force flush)


@router.post(
    "/docs/upload",
    response_model=UploadResponse,
    tags=["ingest"],
    summary="Upload a PDF or text file and index into Chroma",
)
async def upload_document(file: Annotated[UploadFile, File(...)]) -> UploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file name")
    content_type = (file.content_type or "").lower()
    if content_type not in {"application/pdf", "text/plain"} and not file.filename.lower().endswith((".pdf", ".txt", ".md")):
        raise HTTPException(status_code=415, detail="Unsupported media type. Use PDF or text.")

    saved_path = _save_upload(file)
    try:
        docs = _load_documents(saved_path)
        chunks = _split_documents(docs)
        _persist_chunks(chunks)
    except HTTPException:
        # passthrough
        raise
    except Exception as e:
        # Cleanup saved file on failure (best-effort)
        try:
            saved_path.unlink(missing_ok=True)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")

    return UploadResponse(file_name=saved_path.name, chunks=len(chunks), status="ok")
