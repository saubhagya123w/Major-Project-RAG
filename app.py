
from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from typing import List, Optional
import os, json

# import local helpers (we assume running from same folder)
from pathlib import Path
import pickle
import time

# We'll import functions/classes defined in the notebook environment by reloading
# For the simple local setup, we also provide a thin wrapper that reuses the
# vector_store and functions if the notebook started the objects; else we lazy import.

app = FastAPI(title="RAG Website Retrieval API")

# Auth dependency
API_TOKEN = os.getenv("API_TOKEN", "CHANGE_ME_API_TOKEN")
def check_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-KEY header")

class IndexRequest(BaseModel):
    url: List[str]

class ChatMessage(BaseModel):
    content: str
    role: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/api/v1/index")
async def index_endpoint(body: IndexRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    # We'll call functions from the notebook environment if available (for local dev)
    # Try to import helper functions from rag notebook module or rely on index_urls being in globals
    try:
        from __main__ import index_urls
    except Exception:
        raise HTTPException(status_code=500, detail="Indexer functions not found. Start server from notebook or ensure helper functions are accessible.")
    # index the urls
    results = index_urls(body.url)
    return {"status": "success", "indexed_url": results.get("indexed_url", []), "failed_url": results.get("failed_url", None)}

@app.post("/api/v1/chat")
async def chat_endpoint(body: ChatRequest, x_api_key: str = Header(None)):
    check_api_key(x_api_key)
    try:
        from __main__ import generate_answer
    except Exception:
        raise HTTPException(status_code=500, detail="RAG functions not found. Start server from notebook or ensure helper functions are accessible.")
    # Convert pydantic message objects to dicts
    messages = [{"role": m.role, "content": m.content} for m in body.messages]
    try:
        resp = generate_answer(messages)
        return {"response": [{"answer": {"content": resp["answer"], "role": "assistant"}, "citation": resp.get("citations", [])}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
