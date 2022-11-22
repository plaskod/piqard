import json
import os


def directory(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def load_jsonl(path: str) -> list[dict]:
    with open(path, "r") as f:
        data = [json.loads(jline) for jline in f.read().splitlines()]
    return data


def save_results(path: str, results: dict):
    with open(path, "w") as f:
        json.dump(results, f)
