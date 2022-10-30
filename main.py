import argparse
import json

from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.basic_prompt import BasicPrompt
import config
from utils import directory


class PIQARD:
    def __init__(self):
        self.information_retriever = GoogleCustomSearch()
        self.large_language_model = GPTj6bAPI()
        self.prompt_generator = BasicPrompt()

    def __call__(self, query):
        result_dir = directory(config.result_dir)
        retrieved_documents = self.information_retriever.request(query)

        with open(f"{result_dir}/retrieved_documents.txt", "w") as f:
            json.dump(retrieved_documents, f)

        prompt = self.prompt_generator.generate(query)
        generated_answer = self.large_language_model.query(prompt)

        with open(f"{result_dir}/generated_answer.txt", "w") as f:
            json.dump(generated_answer, f)

        print(generated_answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    piqard(args.query)
