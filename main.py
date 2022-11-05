import argparse
import json
import config
from config import PIQARDConfig
from utils import directory
import re

# Dokumentacja API:  https://discuss.huggingface.co/t/strange-answer-from-api/13538

def postprocess_answer(answer: str) -> str:
    return re.sub(r"\.\s.*$", ".", answer)

# write a function with an infinite loop that asks the user for a question and prints the answer
def conversation(model):
    while(True):
        context = ''
        user_input = str(input("Ask assistant: "))
        context += user_input
        model(user_input)
        
class PIQARD:
    def __init__(self):
        self.result_dir = directory(config.result_dir)
        self.large_language_model = PIQARDConfig.large_language_model
        self.prompt_generator = PIQARDConfig.prompt_generator

    def __call__(self, query):
        print(f"=== Prompting strategy: {self.prompt_generator}")
        prompt = self.prompt_generator.generate(query)

        print(f"=== Language model: {self.large_language_model}")
        
        generated_answer = self.large_language_model.query({"inputs": prompt, "return_full_text": False,"max_new_tokens" : 200 })

        # with open(f"{self.result_dir}/generated_answer.txt", "w") as f:
        #     json.dump(generated_answer, f)

        # print the answer only to the first newline character

        split_answer = generated_answer[0]["generated_text"].split("\n")
        last_user_input = f"Human: {query}"
        
        ind = -1
        for i, line in enumerate(split_answer):
            if line == last_user_input:
                ind = i + 1
                break
            
        print(split_answer[ind])
        # next_generated_answer = self.large_language_model.query({"inputs": generated_answer[0]["generated_text"]})
        # print(f"final answer: {next_generated_answer[0]['generated_text']}")
        # nnext_generated_answer = self.large_language_model.query({"inputs": next_generated_answer[0]["generated_text"]})
        # print(f"final answer: {nnext_generated_answer[0]['generated_text']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    conversation(piqard)
    postprocess_answer()
