# RAG Project

This project demonstrates a **Retrieval-Augmented Generation (RAG) system** with a FastAPI API and document indexing functionality.

---

## Description

The project contains:  
1. **FastAPI RAG API** – Provides an endpoint for posting data and indexing it using RAG.  
2. **RAG Indexing Engine** – Handles document preprocessing, embeddings, and query-based retrieval.

---

## Setup

1. Clone the repository:

```bash
git clone <your_github_repo_url>
cd RAG-Project
Create a .env file (based on .env.example) and add your API key:

ini
Copy code
API_TOKEN=your_api_key_here
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run
FastAPI Server
bash
Copy code
uvicorn app:app --reload --port 8000
Test API Endpoint
Endpoint: POST /api/v1/index

Header: X-API-KEY (your API key from .env)

Example with curl:

bash
Copy code
curl -X POST http://127.0.0.1:8000/api/v1/index -H "X-API-KEY: your_api_key_here"
RAG Indexing Engine
bash
Copy code
python main.py
Features
Document preprocessing and cleaning

Vector embeddings for efficient retrieval

API authentication with X-API-KEY

Query-based document retrieval
