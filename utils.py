import json
import os
import tqdm


def directory(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def load_jsonl(path: str) -> list[dict]:
    with open(path, "r") as f:
        data = [json.loads(jline) for jline in tqdm.tqdm(f.read().splitlines())]
    return data


def save_results(path: str, results: dict):
    _ = directory(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(results, f, indent=4)
