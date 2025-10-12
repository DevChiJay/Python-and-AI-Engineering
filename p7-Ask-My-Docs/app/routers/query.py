from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from ..services.llm import get_chat_model
from ..services.qa_chain import build_qa_chain


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str] | None = None


router = APIRouter()


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"


def _get_vectorstore(collection_name: str = "ask_my_docs") -> Chroma:
    if not VECTOR_DIR.exists():
        raise HTTPException(status_code=404, detail="Vector store not found. Please ingest documents first.")
    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    return Chroma(
        embedding_function=embeddings,
        collection_name=collection_name,
        persist_directory=str(VECTOR_DIR),
    )


@router.post(
    "/query/ask",
    response_model=AskResponse,
    tags=["query"],
    summary="Ask a question over the ingested documents",
)
async def ask(req: Annotated[AskRequest, ...]) -> AskResponse:
    question = (req.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    # Connect to persisted Chroma and create a retriever
    store = _get_vectorstore()
    retriever = store.as_retriever(search_kwargs={"k": int(os.getenv("TOP_K", "4"))})

    # Build RetrievalQA chain with custom prompt
    llm = get_chat_model()
    qa_chain = build_qa_chain(llm, retriever)

    try:
        result = qa_chain.invoke({"query": question})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run retrieval QA: {e}")

    answer = result.get("result") or ""
    source_docs = result.get("source_documents") or []
    sources: list[str] = []
    try:
        sources = [str(getattr(d, "metadata", {}).get("source", "")) for d in source_docs]
    except Exception:
        sources = []

    return AskResponse(answer=answer.strip(), sources=[s for s in sources if s])
