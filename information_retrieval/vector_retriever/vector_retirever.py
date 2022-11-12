import pickle

import faiss
from sentence_transformers import SentenceTransformer


class VectorRetriever:
    def __init__(self, documents_path: str, index_path: str):
        self.model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
        self.documents = self.__load_documents(documents_path)
        self.index = self.__load_index(index_path)

    @staticmethod
    def __load_documents(path: str) -> list:
        with open(path) as f:
            return [line.replace("\"", "") for line in f.readlines()]

    @staticmethod
    def __load_index(index_path: str) -> faiss.Index:
        with open(index_path, 'rb') as f:
            return pickle.load(f)

    def get_documents(self, question: str, n: int = 1):
        _, document_indexes = self.index.search(self.model.encode([question]), n)
        retireved_documents = [self.documents[i] for i in document_indexes[0]]
        return retireved_documents
