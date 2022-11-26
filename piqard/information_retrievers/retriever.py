import json
import pickle
from typing import Union

import faiss
import fastbm25
from tqdm import tqdm

from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class Retriever:
    def __init__(self, database: str = None, k: int = 1):
        self.k = k
        if database:
            self.documents = self.__load_documents(
                f"assets/database/{database}/corpus.jsonl"
            )

    @staticmethod
    def __load_documents(path: str) -> list:
        with open(path) as f:
            return [json.loads(jline)["text"] for jline in tqdm(f.read().splitlines())]

    @staticmethod
    def load_index(index_path: str) -> Union[fastbm25.fastbm25, faiss.Index]:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    def get_documents(self, question: str) -> list[str]:
        pass

    def __str__(self):
        return self.__class__.__name__
