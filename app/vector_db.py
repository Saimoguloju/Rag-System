import faiss
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import os

class VectorDB:
    """Handles FAISS operations including indexing, searching, and updating."""

    def __init__(self, index_path: str, model_name: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = self._load_or_initialize_index()

    def _load_or_initialize_index(self):
        """Loads an existing FAISS index or initializes a new one."""
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        else:
            return faiss.IndexFlatL2(self.dimension)

    def add_document(self, filename: str, text: str):
        """Encodes the document text and adds it to the FAISS index."""
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding, dtype=np.float32))
        faiss.write_index(self.index, self.index_path)

    def search(self, query: str, k: int = 5) -> List[Tuple[int, float]]:
        """Searches the FAISS index for the top-k nearest documents."""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), k)
        return list(zip(indices[0], distances[0]))
