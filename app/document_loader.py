from PyPDF2 import PdfReader
import os
from typing import Optional

def load_document(filename: str, content: bytes) -> Optional[str]:
    """Determines the file type and extracts text accordingly."""
    loaders = {
        "pdf": extract_text_from_pdf,
        "txt": extract_text_from_txt
    }
    
    file_ext = filename.split(".")[-1].lower()
    if file_ext in loaders:
        return loaders[file_ext](content)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")

def extract_text_from_pdf(content: bytes) -> str:
    """Extracts text from a PDF file."""
    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(content)
    
    reader = PdfReader(temp_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    
    os.remove(temp_path)
    return text.strip()

def extract_text_from_txt(content: bytes) -> str:
    """Extracts text from a TXT file."""
    return content.decode("utf-8").strip()