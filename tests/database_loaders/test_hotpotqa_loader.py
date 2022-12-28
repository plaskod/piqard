from database_loaders.hotpotqa_loader import *


def test_load_documents() -> None:
    load_documents()


def test_load_questions_1() -> None:
    load_questions()


# test if function can load 5 first questions
def test_load_questions_2() -> None:
    load_questions(number=5)


def test_load_questions_3() -> None:
    load_questions(number=99999999)
