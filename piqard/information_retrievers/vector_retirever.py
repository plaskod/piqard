from sentence_transformers import SentenceTransformer

from piqard.information_retrievers.exceptions import (
    DynamicPromptingNotImplementedException,
)
from piqard.information_retrievers.retriever import Retriever


class VectorRetriever(Retriever):
    def __init__(self, database: str, k: int = 1, n: int = 0):
        super().__init__(database, k, n)
        self.index = self.load_index(f"assets/database/{database}/vector_index.pickle")
        if n > 0:
            try:
                self.question_index = self.load_index(
                    f"assets/database/{database}/question_vector_index.pickle"
                )
            except FileNotFoundError:
                raise DynamicPromptingNotImplementedException(self.__str__())
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str):
        _, document_indexes = self.index.search(self.model.encode([question]), self.k)
        retrieved_documents = [self.documents[i] for i in document_indexes[0]]
        return retrieved_documents

    def get_questions(self, question: str) -> list[dict]:
        _, question_indexes = self.question_index.search(
            self.model.encode([question]), self.n
        )
        retrieved_questions = [self.questions[i] for i in question_indexes[0]]
        return retrieved_questions
