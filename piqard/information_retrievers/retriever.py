import pickle
from typing import Union

import faiss
import fastbm25

from database_loaders.database_loader_factory import DataBaseLoaderFactory
from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class Retriever:
    def __init__(self, database: str = None, k: int = 1, n: int = 0):
        self.k = k
        self.n = n
        if database:
            database_loader = DataBaseLoaderFactory(database)
            self.documents = database_loader.load_documents()
            if n > 0:
                self.questions = database_loader.load_questions()

    @staticmethod
    def load_index(index_path: str) -> Union[fastbm25.fastbm25, faiss.Index]:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    def get_documents(self, question: str) -> list[str]:
        pass

    def get_questions(self, question: str) -> list[dict]:
        pass

    def __call__(self, *args, **kwargs):
        return self.get_documents(*args)

    def __str__(self):
        return self.__class__.__name__

