from unittest.mock import MagicMock

from transformers import BloomTokenizerFast

from piqard.language_models import CohereAPI

class TestCohereAPI():

    def test_init(self, monkeypatch):
        language_model = CohereAPI("stop_token", 50, 0.01, top_k=2)
        assert language_model.stop_token == "stop_token"
        assert language_model.parameters["max_tokens"] == 50
        assert language_model.parameters["temperature"] == 0.01
        assert language_model.parameters["k"] == 2
        assert str(language_model) == "Cohere API"

    def test_query(self):
        language_model = CohereAPI("\n")
        res = language_model.query("payload\nwrite above line 3 times")
        assert isinstance(res, str)