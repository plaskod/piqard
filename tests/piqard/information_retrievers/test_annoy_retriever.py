import os
import pytest
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
from piqard.information_retrievers.retriever import Retriever
from piqard.information_retrievers.annoy_retriever import AnnoyRetriever
from piqard.utils.exceptions import DynamicPromptingNotImplementedException


class TestAnnoyRetriever:
    def test_init(self, monkeypatch):

        def mock_load_jsonl(path):
            return [
                {"_id": 1, "text": "What is the capital of France?", "answer": "Paris"},
                {"_id": 2, "text": "What is the largest planet in our solar system?", "answer": "Jupiter"},
                {"_id": 3, "text": "What is the smallest planet in our solar system?", "answer": "Mercury"}
            ]

        monkeypatch.setattr("piqard.utils.io.load_jsonl.__code__", mock_load_jsonl.__code__)
        # Test that the class initializes correctly

        retriever = AnnoyRetriever(
            database="openbookqa",
            database_index="tests/testAnnoyIndex.ann",
            database_path="tests/database.jsonl",
            questions_index="questions_index.ann",
            questions_path="questions.json",
            k=1,
            n=0,
            dimensions=384,
            sentence_transformer="multi-qa-MiniLM-L6-cos-v1"
        )
        assert isinstance(retriever, AnnoyRetriever)
        assert isinstance(retriever.index, AnnoyIndex)
        assert isinstance(retriever.model, SentenceTransformer)

    def test_dynamic_prompting_not_implemented(self):
        # Test that the class raises an exception when n > 0
        with pytest.raises(DynamicPromptingNotImplementedException):
            retriever = AnnoyRetriever(
                database="openbookqa",
                database_index="tests/testAnnoyIndex.ann",
                database_path="tests/database.jsonl",
                questions_index="questions_index.ann",
                questions_path="tests/questions.jsonl",
                k=1,
                n=1,
                dimensions=384,
                sentence_transformer="multi-qa-MiniLM-L6-cos-v1"
            )

    def test_get_documents(self):
        retriever = AnnoyRetriever(
            database="openbookqa",
            database_index="tests/testAnnoyIndex.ann",
            database_path="tests/database.jsonl",
            k=1,
            n=0,
            dimensions=384,
            sentence_transformer="multi-qa-MiniLM-L6-cos-v1"
        )
        result = retriever.get_documents("bee")
        assert result[0] == 'A bee is a pollinating animal'

    def test_get_questions(self):
        retriever = AnnoyRetriever(
            database="openbookqa",
            database_index="tests/testAnnoyIndex.ann",
            database_path="tests/database.jsonl",
            questions_index="tests/testQuestion.ann",
            questions_path="tests/questions.jsonl",
            k=1,
            n=1,
            dimensions=384,
            sentence_transformer="multi-qa-MiniLM-L6-cos-v1"
        )
        result = retriever.get_questions("bee")
        assert result[0]["text"] == 'What is the fastest cat?'