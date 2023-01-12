from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex


from piqard.information_retrievers.retriever import Retriever
from piqard.utils.exceptions import DynamicPromptingNotImplementedException


class AnnoyRetriever(Retriever):
    """
    Wrapper around Annoy algorithm for information retrieval.
    """

    def __init__(
        self,
        database: str,
        database_index: str = None,
        database_path: str = None,
        questions_index: str = None,
        questions_path: str = None,
        k: int = 1,
        n: int = 0,
    ):
        """
        Constructor for the AnnoyRetriever class.

        :param database: The database name to use. Available database choose [openbookqa, hotpotqa]
        :param database_index: The path to the database index.
        :param database_path: The path to the database.
        :param questions_index: The path to the questions index.
        :param questions_path: The path to the questions.
        :param k: The number of documents to retrieve.
        :param n: The number of questions to retrieve.
        """
        super().__init__(database, database_path, questions_path, k=k, n=n)
        self.index = AnnoyIndex(384, "angular")
        self.index.load(database_index)
        if n > 0:
            try:
                self.question_index.load(questions_index)
            except Exception:
                raise DynamicPromptingNotImplementedException(self.__str__())
        self.model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    def get_documents(self, question: str) -> list[str]:
        """
        Retrieves the documents for the given question.

        :param question: The question to retrieve the documents for.
        :return: The retrieved documents.
        """
        document_indexes = self.index.get_nns_by_vector(
            self.model.encode(question), self.k
        )
        retrieved_documents = [self.documents[i] for i in document_indexes]
        return retrieved_documents

    def get_questions(self, question: str) -> list[dict]:
        """
        Retrieves the questions for the given question.

        :param question: The question to retrieve the questions for.
        :return: The retrieved questions.
        """
        question_indexes = self.index.get_nns_by_vector(
            self.model.encode(question), self.n
        )
        retrieved_questions = [self.questions[i] for i in question_indexes]
        return retrieved_questions

    def __str__(self):
        return "AnnoyRetriever"
