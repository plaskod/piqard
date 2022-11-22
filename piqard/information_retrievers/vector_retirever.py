from sentence_transformers import SentenceTransformer

from piqard.information_retrievers.retriever import Retriever


class VectorRetriever(Retriever):
    def __init__(self, database: str, k: int = 1):
        super().__init__(database, k)
        self.index = self.load_index(f"assets/database/{database}/vectore_index.pickle")
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str):
        _, document_indexes = self.index.search(self.model.encode([question]), self.k)
        retireved_documents = [self.documents[i] for i in document_indexes[0]]
        return retireved_documents
