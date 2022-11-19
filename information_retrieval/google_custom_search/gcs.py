import argparse
import json
import os

import requests
from tqdm import tqdm
from newspaper import Article

from information_retrieval.retriever import Retriever


class GoogleCustomSearch(Retriever):
    def __init__(self, database: str = None):
        super().__init__(database)
        try:
            with open(
                f"{os.path.dirname(os.path.abspath(__file__))}/credentials.json", "r"
            ) as f:
                credentials = json.load(f)
                self.engineID = credentials["engineID"]
                self.APIkey = credentials["APIkey"]
        except (FileNotFoundError, KeyError):
            print(
                "Google Custom Search credentials not found or incorrect file structure."
            )
            exit(0)

    def get_documents(
        self, query: str, n: int = 1, start_date: str = "", end_date: str = ""
    ) -> list:
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={self.APIkey}"
            f"&cx={self.engineID}"
            f"&q={query}"
            f"&start=1"
            f"&num={n}"
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    parser.add_argument("--start-date", type=str, default="", help="Search start date")
    parser.add_argument("--end-date", type=str, default="", help="Search end date")
    parser.add_argument(
        "--out-file", type=str, default="results.txt", help="output jsonl file"
    )
    args = parser.parse_args()

    search_engine = GoogleCustomSearch()
    results = search_engine.get_documents(args.query, args.start_date, args.end_date)
    with open(args.out_file, "w") as f:
        json.dump(results, f)
