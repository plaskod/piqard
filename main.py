import argparse
import json
import config
from config import PIQARDConfig
from utils import directory

# https://discuss.huggingface.co/t/strange-answer-from-api/13538
TEMP_PAYLOAD = {
    "inputs" : "You're a chatbot helping users to keep track of their healthy habits. One of the users didn't engage with the app for a while.  Be as friendly as possible and try to get the user to engage with the app again by asking a question about their latest habit: duolingo. Mention the value of learning new languages. Start now:",
    "max_length" : 500,
}

class PIQARD:
    def __init__(self):
        self.result_dir = directory(config.result_dir)
        self.large_language_model = PIQARDConfig.large_language_model
        self.prompt_generator = PIQARDConfig.prompt_generator

    def __call__(self, query):
        print(f"=== Prompting strategy: {self.prompt_generator}")
        habit = "dancing"
        prompt = self.prompt_generator.generate(habit)

        print(f"=== Language model: {self.large_language_model}")
        
        generated_answer = self.large_language_model.query({"inputs": prompt, "do_sample" : True, "top_k" : 50})

        with open(f"{self.result_dir}/generated_answer.txt", "w") as f:
            json.dump(generated_answer, f)

        print(generated_answer[0]["generated_text"])
        
        next_generated_answer = self.large_language_model.query({"inputs": generated_answer[0]["generated_text"], "do_sample" : True, "top_k" : 50})
        print(f"final answer: {next_generated_answer[0]['generated_text']}")
        nnext_generated_answer = self.large_language_model.query({"inputs": next_generated_answer[0]["generated_text"], "do_sample" : True, "top_k" : 50})
        print(f"final answer: {nnext_generated_answer[0]['generated_text']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--query", type=str, help="query", required=True)
    args = parser.parse_args()

    piqard = PIQARD()
    piqard(args.query)
