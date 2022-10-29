import argparse
import json
import requests
from tqdm import tqdm
from newspaper import Article


class GoogleCustomSearch:
    def __init__(self):
        try:
            with open("credentials.json", "r") as f:
                credentials = json.load(f)
                self.engineID = credentials["engineID"]
                self.APIkey = credentials["APIkey"]
        except (FileNotFoundError, KeyError):
            print(
                "Google Custom Search credentials not found or incorrect file structure."
            )
            exit(0)

    def request(
            self, query: str, start_date: str = "", end_date: str = ""
    ) -> list:
        url = (
            f"https://www.googleapis.com/customsearch/v1?"
            f"key={self.APIkey}"
            f"&cx={self.engineID}"
            f"&q={query}"
            f"&start=1"
            f"&sort=date:r:{start_date}:{end_date}"
        )
        data = requests.get(url).json()
        search_results = data.get("items", [])
        results = []
        for search_result in tqdm(search_results):
            results.append(
                {
                    "title": search_result.get("title"),
                    "url": search_result.get("link")
                } | self.parse_article(search_result.get("link"))
            )

        return results

    @staticmethod
    def parse_article(url: str) -> dict[str, str]:
        article = Article(url)
        article.download()
        article.parse()
        publish_date = article.publish_date
        return {"text": article.text, "publish_date": publish_date.strftime("%Y/%m/%d") if publish_date else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--query', type=str, help='query', required=True)
    parser.add_argument('--start-date', type=str, default='', help='Search start date')
    parser.add_argument('--end-date', type=str, default='', help='Search end date')
    parser.add_argument('--out-file', type=str, default='results.txt', help='output jsonl file')
    args = parser.parse_args()

    search_engine = GoogleCustomSearch()
    results = search_engine.request(args.query, args.start_date, args.end_date)
    with open(args.out_file, "w") as f:
        json.dump(results, f)
