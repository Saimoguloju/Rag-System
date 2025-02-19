import mlflow
import time
from functools import wraps

class MLFlowLogger:
    """Handles logging of performance metrics to MLflow."""
    
    def __init__(self, experiment_name: str = "FAISS_Document_Retrieval"):
        mlflow.set_experiment(experiment_name)

    def log_metric(self, key: str, value: float):
        """Logs a single metric to MLflow."""
        mlflow.log_metric(key, value)

    def log_parameters(self, params: dict):
        """Logs a dictionary of parameters to MLflow."""
        mlflow.log_params(params)

    def track_time(self, func):
        """Decorator to track execution time of functions."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            mlflow.log_metric(f"{func.__name__}_execution_time", elapsed_time)
            return result
        return wrapper
