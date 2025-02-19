import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.document_loader import load_document
from app.vector_db import VectorDB
from config import FAISS_INDEX_PATH

# Initialize the FAISS vector database
vector_db = VectorDB(FAISS_INDEX_PATH)

def process_new_file(file_path: str):
    """Loads and indexes a new document."""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        
        text = load_document(file_path, content)
        vector_db.add_document(os.path.basename(file_path), text)
        print(f"Indexed new document: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

class DocumentHandler(FileSystemEventHandler):
    """Handles new document events."""
    def on_created(self, event):
        if not event.is_directory:
            process_new_file(event.src_path)

if __name__ == "__main__":
    folder_to_watch = "research_papers"
    observer = Observer()
    event_handler = DocumentHandler()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Monitoring {folder_to_watch} for new documents...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
