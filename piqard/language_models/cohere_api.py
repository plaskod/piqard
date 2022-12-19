import json
import cohere
from cohere import CohereError

from piqard.language_models.language_model import LanguageModel


class CohereAPI(LanguageModel):
    def __init__(
        self,
        stop_token: str = None,
        max_tokens: int = 50,
        temperature: float = 0,
        top_k: int = 1,
    ):
        super().__init__(stop_token)
        try:
            with open("assets/credentials/cohere.json", "r") as f:
                self.API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.client = cohere.Client(self.API_KEY)
        self.parameters = {
            "model": "xlarge",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "k": top_k,
        }

    def query(self, payload: str) -> str:
        generated_answer = self.single_query(payload)
        requests_number = 1
        if self.stop_token:
            while generated_answer.find(self.stop_token) == -1 and requests_number < 5:
                requests_number += 1
                generated_text = self.single_query(payload + generated_answer)
                generated_answer += generated_text

        if self.stop_token is None or generated_answer.find(self.stop_token) == -1:
            return generated_answer
        return generated_answer.split(self.stop_token)[0]

    def single_query(self, payload: str) -> str:
        try:
            response = self.client.generate(prompt=payload, **self.parameters)
            return response.generations[0].text.strip().strip("\n")
        except CohereError as e:
            if e.http_status == 598:  # locked output
                return "Error: adjust template; locked output"

    def __str__(self) -> str:
        return "Cohere API"
