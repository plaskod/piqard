import pickle
from typing import Union

import faiss
import fastbm25

from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class Retriever:
    def __init__(self, database: str = None):
        if database:
            self.documents = self.__load_documents(
                f"assets/database/{database}/corpus.txt"
            )

    @staticmethod
    def __load_documents(path: str) -> list:
        with open(path) as f:
            return [line.replace('"', "") for line in f.readlines()]

    @staticmethod
    def load_index(index_path: str) -> Union[fastbm25.fastbm25, faiss.Index]:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    def get_documents(self, question: str, n: int = 1) -> list[str]:
        pass

    def __str__(self):
        return self.__class__.__name__
