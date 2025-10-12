# Ask My Docs

Upload your documents (PDF/TXT/MD), index them into a local Chroma vector store with OpenAI embeddings, and ask questions via a Retrieval-Augmented Generation (RAG) API. The model answers only from the provided context and says “I don’t know” if the answer isn’t found.

## Tech
- FastAPI
- LangChain (split packages v0.3+)
- Chroma (persisted locally)
- OpenAI (chat + embeddings)

## Project layout
- app/routers/ingest.py — upload, chunk, embed, and persist to Chroma
- app/routers/query.py — query over documents via RetrievalQA
- app/services/qa_chain.py — custom prompt and RetrievalQA builder
- data/uploads — saved uploads
- data/vector_store — persisted Chroma collection

## Prerequisites
- Python 3.10+
- OpenAI API key

## Setup
1) Create and activate a virtualenv
2) Install deps (example):
   - pip install fastapi uvicorn langchain langchain-openai langchain-chroma langchain-community langchain-text-splitters python-dotenv pydantic
3) Create .env in project root:
   - OPENAI_API_KEY=sk-...
   - EMBEDDING_MODEL=text-embedding-3-small  (default)
   - TOP_K=4                                (optional)

## Run
- From this folder:
  - uvicorn main:app --reload
- API docs: http://127.0.0.1:8000/docs

## Endpoints
- POST /docs/upload
  - multipart/form-data, field: file (PDF/TXT/MD)
  - Stores chunks in Chroma (data/vector_store)
- POST /query/ask
  - { "question": "..." }
  - Returns { answer, sources[] }
- GET /health

## Examples
- Upload:
  - curl -F "file=@/path/to/file.pdf" http://127.0.0.1:8000/docs/upload
- Ask:
  - curl -X POST http://127.0.0.1:8000/query/ask -H "Content-Type: application/json" -d "{\"question\":\"What is X?\"}"

## Test page
- Open test/index.html in a browser to upload files via a simple UI.

## Notes
- If you see “Vector store not found”, upload a document first.
- Delete data/vector_store to reset the index.
- Sources come from document metadata (source filename).
