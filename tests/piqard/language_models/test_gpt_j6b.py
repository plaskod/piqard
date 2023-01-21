from unittest.mock import MagicMock

from transformers import BloomTokenizerFast, AutoTokenizer

from piqard.language_models import GPTj6bAPI

class TestGPTj6bAPI():

    def test_init(self, monkeypatch):
        language_model = GPTj6bAPI("stop_token")
        assert language_model.stop_token == "stop_token"
        assert str(language_model) == "GPT-J6B huggingface.co API"

    def test_query(self):
        language_model = GPTj6bAPI("\n")
        res = language_model.query("can you tell me a long joke?")
        assert isinstance(res, str)

    def test_preprocess_cut(self):
        with open('tests/LoremIpsum.txt', 'r') as file:
            prompt = file.read().replace('\n', '')
        language_model = GPTj6bAPI("\n")
        new_prompt = language_model.preprocess_prompt(prompt)
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        assert len(tokenizer(new_prompt)["input_ids"]) <= 2048