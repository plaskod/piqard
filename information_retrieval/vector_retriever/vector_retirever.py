from sentence_transformers import SentenceTransformer

from information_retrieval.retriever import Retriever


class VectorRetriever(Retriever):
    def __init__(self, database: str):
        super().__init__(database)
        self.index = self.load_index(f"assets/database/{database}/vectore_index.pickle")
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str, n: int = 1):
        _, document_indexes = self.index.search(self.model.encode([question]), n)
        retireved_documents = [self.documents[i] for i in document_indexes[0]]
        return retireved_documents
