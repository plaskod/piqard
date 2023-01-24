import json
import os
from tqdm.notebook import tqdm

from piqard.utils.exceptions import EnvironmentVariableNotSet


def directory(path: str) -> str:
    """
    Create a directory if it does not exist.

    :param path: Path to the directory.
    :return: Path to the directory.
    """
    os.makedirs(path, exist_ok=True)
    return path


def load_jsonl(path: str) -> list[dict]:
    """
    Load jsonl file.

    :param path: Path to the jsonl file.
    :return: List of dictionaries.
    """
    file_name = path.split("/")[-1]
    with open(path, "r") as f:
        data = [
            json.loads(jline)
            for jline in tqdm(f.read().splitlines(), desc=f"{file_name}")
        ]
    return data


def save_results(path: str, results: dict) -> None:
    """
    Save results to a specified path.

    :param path: Path to the results.
    :param results: Dictionary with results.
    :return: None.
    """
    _ = directory(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(results, f, indent=4)


def get_env_variable(name: str) -> str:
    """
    Get environment variable.

    :param name: Name of the environment variable.
    :return: Value of the environment variable.
    """
    try:
        return os.environ[name]
    except KeyError:
        raise EnvironmentVariableNotSet(name)
