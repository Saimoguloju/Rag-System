import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from monitoring.processing import process_document

class DocumentHandler(FileSystemEventHandler):
    """Handles new document events and processes them."""
    def on_created(self, event):
        if not event.is_directory:
            print(f"New document detected: {event.src_path}")
            process_document(event.src_path)

if __name__ == "__main__":
    folder_to_watch = "research_papers"
    os.makedirs(folder_to_watch, exist_ok=True)  # Ensure folder exists
    
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
