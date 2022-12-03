import json
import os

import requests
from tqdm import tqdm
from newspaper import Article

from piqard.information_retrievers.exceptions import DynamicPromptingNotImplementedException
from piqard.information_retrievers.retriever import Retriever


class GoogleCustomSearch(Retriever):
    def __init__(self, database: str = None, k: int = 1, n: int = 0):
        super().__init__(database, k)
        try:
            with open(
                "assets/credentials/google_custom_search.json", "r"
            ) as f:
                credentials = json.load(f)
                self.engineID = credentials["engineID"]
                self.APIkey = credentials["APIkey"]
        except (FileNotFoundError, KeyError):
            print(
                "Google Custom Search credentials not found or incorrect file structure."
            )
            exit(0)

        if n > 0:
            raise DynamicPromptingNotImplementedException(self.__str__())

    def get_documents(
        self, query: str, start_date: str = "", end_date: str = ""
    ) -> list:
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={self.APIkey}"
            f"&cx={self.engineID}"
            f"&q={query}"
            f"&start=1"
            f"&num={self.k}"
            f"&sort=date:r:{start_date}:{end_date}"
        )
        data = requests.get(url).json()
        search_results = data.get("items", [])
        results = []
        for search_result in tqdm(search_results, disable=(__name__ != "__main__")):
            results.append(self.parse_article(search_result.get("link")))

        return results

    @staticmethod
    def parse_article(url: str) -> dict[str, str]:
        article = Article(url)
        article.download()
        article.parse()
        return article.text

    def __str__(self):
        return "GoogleCustomSearch"
