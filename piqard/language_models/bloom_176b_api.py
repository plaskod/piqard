import json
import requests
from transformers import BloomTokenizerFast

from piqard.language_models.exceptions import Response500Exception, LanguageModelAPIOverloadException
from piqard.language_models.language_model import (
    LanguageModel,
)


class BLOOM176bAPI(LanguageModel):
    def __init__(self, stop_token: str = None, temperature: float = 0.000001, top_k: float = 1):
        super().__init__(stop_token)
        self.tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom")
        try:
            with open("assets/credentials/huggingface.json", "r") as f:
                self.API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.parameters = {"use_cache": False, "temperature": temperature, "top_k": top_k}

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
        return "BLOOM 176b huggingface.co API"

    def preprocess_prompt(self, prompt: str) -> str:
        tokenized = self.tokenizer(prompt)['input_ids']
        prompt_len = len(tokenized)
        if prompt_len > 1000:
            return self.tokenizer.decode(tokenized[-1000:])
        return prompt
