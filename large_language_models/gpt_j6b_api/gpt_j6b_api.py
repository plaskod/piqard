import argparse
import json
import os
import requests


class GPTj6bAPI:
    def __init__(self):
        try:
            with open(f"{os.path.dirname(os.path.abspath(__file__))}/api_key.json", "r") as f:
                API_KEY = json.load(f)['APIkey']
        except (FileNotFoundError, KeyError):
            print(
                "api_key.json not found or incorrect file structure."
            )
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.headers = {"Authorization": f"Bearer {API_KEY}"}

    def query(self, payload: str) -> str:
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--query', type=str, help='query', required=True)
    parser.add_argument('--out-file', type=str, default='results.txt', help='output json file')
    args = parser.parse_args()

    model = GPTj6bAPI()
    results = model.query(args.query)
    with open(args.out_file, "w") as f:
        json.dump(results, f)
