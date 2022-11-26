import json
import os
import requests

from piqard.language_models.language_model import LanguageModel


class BLOOM176bAPI(LanguageModel):
    def __init__(self):
        try:
            with open(
                "assets/credentials/huggingface.json", "r"
            ) as f:
                API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.headers = {"Authorization": f"Bearer {API_KEY}"}
        self.options = {"temperature": 1.0, "do_sample": False}

    def query(self, payload: str) -> str:
        response = requests.post(self.API_URL, headers=self.headers, json={'inputs': payload, "parameters": self.options})
        return response.json()

    def __str__(self) -> str:
        return "BLOOM 176b huggingface.co API"
