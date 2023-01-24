from unittest.mock import MagicMock

from transformers import BloomTokenizerFast

from piqard.language_models import BLOOM176bAPI

class TestBLOOM176bAPI():

    def test_init(self, monkeypatch):
        language_model = BLOOM176bAPI("stop_token", 0.01, top_k=2)
        assert language_model.stop_token == "stop_token"
        assert language_model.parameters["temperature"] == 0.01
        assert language_model.parameters["top_k"] == 2
        assert str(language_model) == "BLOOM 176b huggingface.co API"

    def test_query(self):
        language_model = BLOOM176bAPI("\n")
        res = language_model.query("payload")
        assert isinstance(res, str)

    def test_preprocess_cut(self):
        with open('tests/LoremIpsum.txt', 'r') as file:
            prompt = file.read().replace('\n', '')
        language_model = BLOOM176bAPI("\n")
        new_prompt = language_model.preprocess_prompt(prompt)
        tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom")
        assert len(tokenizer(new_prompt)["input_ids"]) <= 1000


