import argparse
import json
import os
import requests

class BLOOM176bAPI:
    def __init__(self):
        try:
            with open(
                f"{os.path.dirname(os.path.abspath(__file__))}/api_key.json", "r"
            ) as f:
                API_KEY = json.load(f)["APIkey"]
        except (FileNotFoundError, KeyError):
            print("api_key.json not found or incorrect file structure.")
            exit(0)
        self.API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.headers = {"Authorization": f"Bearer {API_KEY}"}

    def query(self, payload: str) -> str:
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()

    def __str__(self) -> str:
        return "BLOOM 176b huggingface.co API"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--query", type=str, help="query", required=True)
    parser.add_argument(
        "--out-file", type=str, default="results.txt", help="output json file"
    )
    args = parser.parse_args()

    print("Connecting to huggingface.co bloom API...")
    model = BLOOM176bAPI()
    results = model.query(args.query)
    print("Response received")
    with open(args.out_file, "w") as f:
        json.dump(results, f)
