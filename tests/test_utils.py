from utils import *


def test_directory() -> None:
    directory("test_directory_to_remove")


def test_load_jsonl() -> None:
    load_jsonl("assets/database/openbookqa/corpus.jsonl")

def test_save_results() -> None:
    save_results("./result/pytest_test.json", {"key": "value"})
