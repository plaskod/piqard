import requests
from tqdm import tqdm
from newspaper import Article

from piqard.utils.exceptions import DynamicPromptingNotImplementedException
from piqard.information_retrievers.retriever import Retriever
from piqard.utils.io import get_env_variable


class GoogleCustomSearch(Retriever):
    """
    Wrapper around Google Custom Search API.

    To use, you should have the environment variables ``GOOGLE_CUSTOM_SEARCH_API_KEY`` and
    ``GOOGLE_CUSTOM_SEARCH_ENGINE_ID`` set with your API key and Engine id.
    """

    def __init__(self, database: str = None, k: int = 1, n: int = 0):
        """
        Constructor for the GoogleCustomSearch class.

        :param database: The database name to use. WARNING GoogleCustomSearch does not support this parameter.
        :param k: The number of documents to retrieve.
        :param n: The number of questions to retrieve. WARNING GoogleCustomSearch does not support this parameter.
        """
        super().__init__(database, k=k)
        self.engineID = get_env_variable("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")
        self.APIkey = get_env_variable("GOOGLE_CUSTOM_SEARCH_API_KEY")

        if n > 0:
            raise DynamicPromptingNotImplementedException(self.__str__())

    def get_documents(self, question: str) -> list[str]:
        """
        Retrieves the documents for the given question.

        :param question: The question to retrieve the documents for.
        :return: The retrieved documents.
        """
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={self.APIkey}"
            f"&cx={self.engineID}"
            f"&q={question}"
            f"&start=1"
            f"&num={self.k}"
        )
        data = requests.get(url).json()
        search_results = data.get("items", [])
        results = []
        for search_result in tqdm(search_results, disable=(__name__ != "__main__")):
            results.append(self.parse_article(search_result.get("link")))

        return results

    @staticmethod
    def parse_article(url: str) -> str:
        """
        Parses the article from the given url.

        :param url: The url to parse the article from.
        :return: The parsed article.
        """
        article = Article(url)
        article.download()
        article.parse()
        return article.text

    def __str__(self):
        return "GoogleCustomSearch"
