from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import faiss
import numpy as np
import os
from document_loader import load_document
from vector_db import VectorDB
from config import FAISS_INDEX_PATH

app = FastAPI()

# Initialize FAISS database
vector_db = VectorDB(FAISS_INDEX_PATH)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FAISS-powered document retrieval API"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a document, extracts text, generates embeddings, and updates FAISS."""
    try:
        content = await file.read()
        text = load_document(file.filename, content)
        vector_db.add_document(file.filename, text)
        return {"message": "File processed and indexed successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/")
def search_documents(query: str, k: int = 5):
    """Searches the FAISS index and returns the most relevant documents."""
    try:
        results = vector_db.search(query, k)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
