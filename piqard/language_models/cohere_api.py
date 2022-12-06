import json
import cohere
from cohere import CohereError

from piqard.language_models.language_model import LanguageModel


class CohereAPI(LanguageModel):
    def __init__(self, stop_token: str = None):
        super().__init__(stop_token)
        try:
            with open("assets/credentials/cohere.json", "r") as f:
                self.API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.client = cohere.Client(self.API_KEY)
        self.parameters = {"model": 'xlarge',
                           "max_tokens": 50,
                           "temperature": 0,
                           "k": 1} | {"stop_sequences": [self.stop_token]} if self.stop_token is not None else {}

    def query(self, payload: str) -> str:
        try:
            response = self.client.generate(prompt=payload, **self.parameters)
            return response.generations[0].text.replace(self.stop_token, "").strip().strip("\n")
        except CohereError as e:
            if e.http_status == 598:# locked output
                return "Error: adjust template; locked output"

    def __str__(self) -> str:
        return "Cohere API"
