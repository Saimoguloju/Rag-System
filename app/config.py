import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FAISS index storage path
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index.index")

# MLflow experiment name
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "FAISS_Document_Retrieval")

# Model name for generating embeddings
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
