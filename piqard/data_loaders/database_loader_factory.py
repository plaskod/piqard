import importlib


class DatabaseLoaderFactory:
    def __init__(self, database: str):

        module = importlib.import_module(f".{database}_loader", package=f"piqard.data_loaders")

        self.load_documents = getattr(module, f"load_documents")
        self.load_questions = getattr(module, f"load_questions")
