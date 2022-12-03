import importlib


class DataBaseLoaderFactory:
    def __init__(self, database: str):
        try:
            module = importlib.import_module(f"database_loaders.{database}_loader")
        except (ImportError, AttributeError):
            raise ValueError(f"Unknown database {database}") from None

        self.load_documents = getattr(module, f"load_documents")
        self.load_questions = getattr(module, f"load_questions")


