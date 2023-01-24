import pytest
from piqard.utils.answer_postprocess import *

def test_answer_is_none() -> None:
    result = postprocess_answer(None)
    assert result == "None"

def test_answer_postprocess() -> None:
    test_string = "    Test Lorem Impsum\ndolor sit amet   "

    result = postprocess_answer(test_string)
    assert result == "Test Lorem Impsum\ndolor sit amet"

def test_answer_postprocess_with_fix_text() -> None:
    test_string = "    So the answer is: Test Lorem Impsum\ndolor sit amet   "
    fix_text = "So the answer is: "

    result = postprocess_answer(test_string, fix_text)
    assert result == "Test Lorem Impsum\ndolor sit amet"