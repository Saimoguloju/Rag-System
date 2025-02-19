from app.document_loader import load_document
from app.vector_db import VectorDB
from config import FAISS_INDEX_PATH
import os

def process_document(file_path: str):
    """Processes a new document, extracts text, and updates the FAISS index."""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        text = load_document(file_path, content)
        vector_db = VectorDB(FAISS_INDEX_PATH)
        vector_db.add_document(os.path.basename(file_path), text)
        print(f"Successfully processed and indexed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")