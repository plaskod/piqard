import os


def directory(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path
