from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from piqard.information_retrievers.retriever import Retriever


class AnnoyRetriever(Retriever):
    def __init__(self, database: str, k: int = 1):
        super().__init__(database, k)
        self.index = AnnoyIndex(384, 'angular')
        self.index.load(f"assets/database/{database}/annoy_index_384.ann")
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str):
        document_indexes = self.index.get_nns_by_vector(self.model.encode(question), self.k)
        retireved_documents = [self.documents[i] for i in document_indexes]
        return retireved_documents
