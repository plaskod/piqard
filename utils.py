import json
import os
import string


def directory(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def load_jsonl(path: str) -> list[dict]:
    with open(path, 'r') as f:
        data = [json.loads(jline) for jline in f.read().splitlines()]
    return data


def save_results(path: str, results: dict):
    with open(path, 'w') as f:
        json.dump(results, f)


def normalize_answer(answer: str) -> str:
    def remove_counter(text):
        return text.replace("年", "").replace("歳", "").replace("人", "").replace("년", "")

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_counter(remove_punc(lower(answer))))
