import json
import os
import requests

from piqard.language_models.language_model import LanguageModel


class GPTj6bAPI(LanguageModel):
    def __init__(self):
        super().__init__()
        try:
            with open(
                "assets/credentials/huggingface.json", "r"
            ) as f:
                API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.headers = {"Authorization": f"Bearer {API_KEY}"}

    def query(self, payload: str) -> str:
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()

    def __str__(self) -> str:
        return "GPT-J6B huggingface.co API"
