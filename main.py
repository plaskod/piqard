import argparse
import json
import config
from config import PIQARDConfig
from utils import directory


class PIQARD:
    def __init__(self):
        self.result_dir = directory(config.result_dir)
        self.information_retriever = PIQARDConfig.information_retriever
        self.large_language_model = PIQARDConfig.large_language_model
        self.prompt_generator = PIQARDConfig.prompt_generator

    def __call__(self, query):

        print(f"=== Information retriever: {self.information_retriever}")
        context = None
        if self.information_retriever:
            retrieved_documents = self.information_retriever.request(query)

            with open(f"{self.result_dir}/retrieved_documents.txt", "w") as f:
                json.dump(retrieved_documents, f)

            context = " ".join(retrieved_documents[0]['text'].split()[:100])

        print(f"=== Prompting strategy: {self.prompt_generator}")
        prompt = self.prompt_generator.generate(query, context)

        print(f"=== Language model: {self.large_language_model}")
        generated_answer = self.large_language_model.query(prompt)

        with open(f"{self.result_dir}/generated_answer.txt", "w") as f:
            json.dump(generated_answer, f)

        print(generated_answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    piqard(args.query)
