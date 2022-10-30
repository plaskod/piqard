import argparse
import json

from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
import config
from utils import directory


class PIQARD:
    def __init__(self):
        self.information_retriever = GoogleCustomSearch()

    def __call__(self, query):
        result_dir = directory(config.result_dir)
        retrieved_documents = self.information_retriever.request(query)

        with open(f"{result_dir}/retrieved_documents.txt", "w") as f:
            json.dump(retrieved_documents, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--query', type=str, help='query', required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    piqard(args.query)

