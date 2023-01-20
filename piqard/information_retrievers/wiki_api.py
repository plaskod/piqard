import wikipedia
from piqard.utils.exceptions import DynamicPromptingNotImplementedException
from piqard.information_retrievers.retriever import Retriever


class WikiAPI(Retriever):
    """
    Wrapper around Wikipedia API.
    """

    def __init__(self, database: str = None, k: int = 1, n: int = 0):
        """
        Constructor for the WikiAPI class.

        :param database: The database name to use. WARNING WikiAPI does not support this parameter.
        :param k: The number of documents to retrieve.
        :param n: The number of questions to retrieve.
        """
        super().__init__(database, k=k)
        if n > 0:
            raise DynamicPromptingNotImplementedException(self.__str__())

    def get_documents(self, question: str):
        """
        Retrieves the documents for the given question.

        :param question: The question to retrieve the documents for.
        :return: The retrieved documents.
        """
        try:
            most_relevant_page = wikipedia.page(question, auto_suggest=False)
            return [wikipedia.summary(most_relevant_page, sentences=self.k).replace("==", "").replace("===", "").replace("\n", " ")]
        except wikipedia.exceptions.PageError as e:
            possible_results = wikipedia.search(f"[{question}]")
            return [f"Could not find {question}. Similar: {possible_results[:5]}."]
        except wikipedia.exceptions.DisambiguationError as e:
            possible_results = wikipedia.search(f"[{question}]")
            return [f"Could not find {question}. Similar: {possible_results[:5]}."]

    def __str__(self):
        return "WikiAPI"
