from unittest.mock import MagicMock

from piqard.language_models.language_model import LanguageModel

class TestFAISSRetriever():
    def test_init(self):
        language_model = LanguageModel("test")
        language_model.query("test")
        assert language_model.stop_token == "test"
        assert str(language_model) == "LanguageModel"
