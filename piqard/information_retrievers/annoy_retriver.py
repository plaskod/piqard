from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

from piqard.information_retrievers.exceptions import (
    DynamicPromptingNotImplementedException,
)
from piqard.information_retrievers.retriever import Retriever


class AnnoyRetriever(Retriever):
    def __init__(self, database: str, k: int = 1, n: int = 0):
        super().__init__(database, k, n)
        self.index = AnnoyIndex(384, "angular")
        self.index.load(f"assets/database/{database}/annoy_index_384.ann")
        if n > 0:
            try:
                self.question_index.load(
                    f"assets/database/{database}/question_annoy_index_384.ann"
                )
            except FileNotFoundError:
                raise DynamicPromptingNotImplementedException(self.__str__())
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str):
        document_indexes = self.index.get_nns_by_vector(
            self.model.encode(question), self.k
        )
        retrieved_documents = [self.documents[i] for i in document_indexes]
        return retrieved_documents

    def get_questions(self, question: str) -> list[dict]:
        question_indexes = self.index.get_nns_by_vector(
            self.model.encode(question), self.n
        )
        retrieved_questions = [self.questions[i] for i in question_indexes]
        return retrieved_questions
