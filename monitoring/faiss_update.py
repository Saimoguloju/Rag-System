from app.vector_db import VectorDB
from config import FAISS_INDEX_PATH
import os

def update_faiss_index(folder_path: str):
    """Updates the FAISS index with all documents in the specified folder."""
    vector_db = VectorDB(FAISS_INDEX_PATH)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                
                from app.document_loader import load_document
                text = load_document(filename, content)
                vector_db.add_document(filename, text)
                print(f"Updated FAISS index with: {filename}")
            except Exception as e:
                print(f"Error updating FAISS index for {filename}: {e}")

if __name__ == "__main__":
    research_papers_folder = "research_papers"
    update_faiss_index(research_papers_folder)