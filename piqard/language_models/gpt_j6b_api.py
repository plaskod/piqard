import requests
from transformers import AutoTokenizer

from piqard.language_models.exceptions import Response500Exception, LanguageModelAPIOverloadException
from piqard.language_models.language_model import LanguageModel
from piqard.utils.io import get_env_variable


class GPTj6bAPI(LanguageModel):
    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        self.API_KEY = get_env_variable("HUGGINGFACE_API_KEY")
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.parameters = {"use_cache": False}

    def query(self, payload: str) -> str:
        generated_answer = self.single_query(self.preprocess_prompt(payload))
        requests_number = 1
        if self.stop_token:
            while generated_answer.find(self.stop_token) == -1 and requests_number < 5:
                requests_number += 1
                prompt = self.preprocess_prompt(payload + generated_answer)
                generated_text = self.single_query(prompt)
                generated_answer += generated_text
        if self.stop_token is None or generated_answer.find(self.stop_token) == -1:
            return generated_answer
        return generated_answer.split(self.stop_token)[0]

    def single_query(self, payload: str) -> str:
        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            json={"inputs": payload, "parameters": self.parameters},
        )
        if response.status_code == 500:
            raise Response500Exception(self.__str__())

        data = response.json()
        if type(data) == dict and "error" in data.keys():
            raise LanguageModelAPIOverloadException(self.__str__())
        return data[0]["generated_text"].split(payload)[1]

    def __str__(self) -> str:
        return "GPT-J6B huggingface.co API"


    def preprocess_prompt(self, prompt: str) -> str:
        tokenized = self.tokenizer(prompt)["input_ids"]
        prompt_len = len(tokenized)
        if prompt_len > 2048:
            return self.tokenizer.decode(tokenized[-2048:])
        return prompt
