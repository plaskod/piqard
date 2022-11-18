import argparse
import json
import config
from config import PIQARDConfig
from prompting.prompt_generator import PromptGenerator
from utils import directory

import logging
logger = logging.getLogger(__name__)

class PIQARD:
    def __init__(self):
        self.result_dir = directory(config.result_dir)
        self.information_retriever = PIQARDConfig.information_retriever
        self.context_builder = PIQARDConfig.context_builder
        self.large_language_model = PIQARDConfig.large_language_model
        self.prompt_template = PromptGenerator.load_template(PIQARDConfig.prompt_template)
        logger.info(f"Information retriever: {self.information_retriever}")
        logger.info(f"Language model: {self.large_language_model}")

    def __call__(self, query: str) -> dict:
        context = None
        if self.information_retriever:
            retrieved_documents = self.information_retriever.get_documents(query, n=5)
            context = self.context_builder.build(retrieved_documents)

        prompt = self.prompt_template.render(question=query,
                                             context=context)

        generated_answer = self.large_language_model.query(prompt)

        final_answer = generated_answer[0]['generated_text'][len(prompt):]

        return {"prompt": prompt, "answer": final_answer, "context": context}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    result = piqard(args.query)

    with open(f"{config.result_dir}/generated_result.txt", "w") as f:
        json.dump(result, f)
    print(result['answer'])
