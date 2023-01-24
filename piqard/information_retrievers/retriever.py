import pickle
from typing import Union
import faiss
import fastbm25

from piqard.utils.data_loaders.database_loader_factory import DatabaseLoaderFactory
from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class Retriever:
    """
    Retriever is an abstract class that represents an information retriever.
    """

    def __init__(
        self,
        database: str = None,
        database_path: str = None,
        questions_path: str = None,
        k: int = 1,
        n: int = 0,
    ):
        """
        Constructor for the Retriever class.

        :param database: The database name to use. Available database choose [openbookqa, hotpotqa]
        :param database_path: The path to the database.
        :param questions_path: The path to the questions.
        :param k: The number of documents to retrieve.
        :param n: The number of questions to retrieve.
        """
        self.k = k
        self.n = n
        if database:
            database_loader = DatabaseLoaderFactory(database)
            self.documents = database_loader.load_documents(database_path)
            if n > 0:
                self.questions = database_loader.load_questions(questions_path)

    @staticmethod
    def load_index(index_path: str) -> Union[fastbm25.fastbm25, faiss.Index]:
        """
        Loads the index from the given path.

        :param index_path: The path to the index.
        :return: The index.
        """
        with open(index_path, "rb") as f:
            return pickle.load(f)

    def get_documents(self, question: str) -> list[str]:
        """
        Retrieves the documents for the given question.

        :param question: The question to retrieve the documents for.
        :return: The retrieved documents.
        """
        pass

    def get_questions(self, question: str) -> list[dict]:
        """
        Retrieves the questions for the given question.

        :param question: The question to retrieve the questions for.
        :return: The retrieved questions.
        """
        pass

    def __call__(self, *args, **kwargs):
        return self.get_documents(*args)

    def __str__(self):
        return self.__class__.__name__
