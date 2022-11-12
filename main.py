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
        self.print_info()

    def print_info(self):
        print(f"=== Information retriever: {self.information_retriever}")
        print(f"=== Prompting strategy: {self.prompt_generator}")
        print(f"=== Language model: {self.large_language_model}")

    def __call__(self, query: str) -> dict:
        context = None
        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query)
            context = " ".join(retrieved_documents[0].split()[:100])

        prompt = self.prompt_generator.generate(query, context)
        generated_answer = self.large_language_model.query(prompt)

        final_answer = generated_answer[0]['generated_text'][len(prompt):]

        return {"answer": final_answer, "context": context}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    result = piqard(args.query)

    with open(f"{config.result_dir}/generated_result.txt", "w") as f:
        json.dump(result, f)
    print(result['answer'])
