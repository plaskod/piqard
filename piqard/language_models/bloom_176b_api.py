import json
import requests

from piqard.language_models.language_model import (
    LanguageModel,
    LanguageModelAPIOverloadException,
)


class BLOOM176bAPI(LanguageModel):
    def __init__(self):
        try:
            with open("assets/credentials/huggingface.json", "r") as f:
                self.API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.parameters = {"use_cache": False, "temperature": 0.000001, "top_k": 1}

    def query(self, payload: str) -> str:
        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            json={"inputs": payload, "parameters": self.parameters},
        )
        data = response.json()
        if type(data) == dict and "error" in data.keys():
            raise LanguageModelAPIOverloadException
        return data

    def __str__(self) -> str:
        return "BLOOM 176b huggingface.co API"
