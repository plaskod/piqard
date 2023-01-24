import json
import os
from tempfile import NamedTemporaryFile
from piqard.utils.data_loaders.hotpotqa_loader import load_questions, load_documents
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

    # Test that the documents are loaded correctly
    documents = load_documents("path/to/documents.jsonl")
    assert len(documents) == 3
    assert documents[0] == "Document 1 text"
    assert documents[1] == "Document 2 text"
    assert documents[2] == "Document 3 text"


def test_load_questions_with_valid_input(monkeypatch):
    # Create a mock load_jsonl function
    def mock_load_jsonl(path):
        return [
            {"_id": 1, "question": "What is the capital of France?", "answer": "Paris"},
            {"_id": 2, "question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
            {"_id": 3, "question": "What is the smallest planet in our solar system?", "answer": "Mercury"}
        ]

    monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)

    # Test that the questions are loaded correctly
    questions = load_questions("path/to/questions.jsonl", number=3)
    assert len(questions) == 3
    assert questions[0]["id"] == 1
    assert questions[0]["text"] == "What is the capital of France?"
    assert questions[0]["possible_answers"] == None
    assert questions[0]["answer"] == "Paris"
    assert questions[1]["id"] == 2
    assert questions[1]["text"] == "What is the largest planet in our solar system?"
    assert questions[1]["possible_answers"] == None
    assert questions[1]["answer"] == "Jupiter"
    assert questions[2]["id"] == 3
    assert questions[2]["text"] == "What is the smallest planet in our solar system?"
    assert questions[2]["possible_answers"] == None
    assert questions[2]["answer"] == "Mercury"
