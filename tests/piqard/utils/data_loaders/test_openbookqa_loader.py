import json
import os
from tempfile import NamedTemporaryFile
from piqard.utils.data_loaders.openbookqa_loader import load_questions, load_documents
from _pytest.monkeypatch import monkeypatch

def test_load_documents_with_valid_input(monkeypatch):
    # Create a mock load_jsonl function
    def mock_load_jsonl(path):
        return [
            {"id": 1, "text": "Document 1 text"},
            {"id": 2, "text": "Document 2 text"},
            {"id": 3, "text": "Document 3 text"},
        ]

    monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

    documents = load_documents("path/to/documents.jsonl")
    assert len(documents) == 3
    assert documents[0] == "Document 1 text"
    assert documents[1] == "Document 2 text"
    assert documents[2] == "Document 3 text"


def test_load_questions_with_valid_input(monkeypatch):
    # Create a mock load_jsonl function
    def mock_load_jsonl(path):
        return [
            {
                "id": 1,
                "question": {
                    "stem": "What is the capital of France?",
                    "choices": [
                        {"label": "A", "text": "Paris"},
                        {"label": "B", "text": "London"},
                        {"label": "C", "text": "Berlin"},
                    ],
                },
                "answerKey": "A",
            },
            {
                "id": 2,
                "question": {
                    "stem": "What is the largest planet in our solar system?",
                    "choices": [
                        {"label": "A", "text": "Jupiter"},
                        {"label": "B", "text": "Earth"},
                        {"label": "C", "text": "Mars"},
                    ],
                },
                "answerKey": "A",
            },
        ]

    monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

    # Test that the questions are loaded correctly
    questions = load_questions("path/to/questions.jsonl", number=2)
    assert len(questions) == 2
    assert questions[0]["id"] == 1
    assert questions[0]["text"] == "What is the capital of France?"
    assert questions[0]["possible_answers"] == "A. Paris B. London C. Berlin"
    assert questions[0]["answer"] == "A. Paris "
    assert questions[1]["id"] == 2
    assert questions[1]["text"] == "What is the largest planet in our solar system?"
    assert questions[1]["possible_answers"] == "A. Jupiter B. Earth C. Mars"
    assert questions[1]["answer"] == "A. Jupiter "

