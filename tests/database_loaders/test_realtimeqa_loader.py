import pytest

from database_loaders.realtimeqa_loader import *


def test_load_documents() -> None:
    with pytest.raises(NotImplementedError):
        load_documents()


def test_load_questions_1() -> None:
    load_questions()


# test if function can load 5 first questions
def test_load_questions_2() -> None:
    load_questions(number=5)


def test_load_questions_3() -> None:
    load_questions(number=99999999)
