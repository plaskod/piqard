import requests
from transformers import BloomTokenizerFast

from piqard.utils.exceptions import (
    Response500Exception,
    LanguageModelAPIOverloadException,
)
from piqard.language_models.language_model import LanguageModel
from piqard.utils.io import get_env_variable


class BLOOM176bAPI(LanguageModel):
    """
    Wrapper around BLOOM 176b large language model huggingface.co API.

    To use, you should have the environment variable ``HUGGINGFACE_API_KEY`` set with your API key
    """

    def __init__(
        self, stop_token: str = None, temperature: float = 0.000001, top_k: float = 1
    ):
        """
        Constructor for the BLOOM 176b huggingface.co API wrapper.

        :param stop_token: The token that indicates the end of the answer.
        :param temperature: The temperature of the language model.
        :param top_k: Number of most likely tokens to consider for generation at each step.
        """
        super().__init__(stop_token)
        self.tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom")
        self.API_KEY = get_env_variable("HUGGINGFACE_API_KEY")
        self.API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
        self.parameters = {
            "use_cache": False,
            "temperature": temperature,
            "top_k": top_k,
        }

    def query(self, payload: str) -> str:
        """
        Gather the partial answers from the language model and return the full answer.

        :param payload: The payload to query the language model with.
        :return: The answer generated by the language model.
        """
        generated_answer = self.single_query(self.preprocess_prompt(payload))
        requests_number = 1
        if self.stop_token:
            while generated_answer.find(self.stop_token) == -1 and requests_number < 5:
                requests_number += 1
                prompt = self.preprocess_prompt(payload + generated_answer)
                generated_text = self.single_query(prompt)
                generated_answer += generated_text
        if self.stop_token is None or generated_answer.find(self.stop_token) == -1:
            return generated_answer
        return generated_answer.split(self.stop_token)[0]

    def single_query(self, payload: str) -> str:
        """
        Queries the language model with the given payload.

        :param payload: The payload to query the language model with.
        :return: The answer generated by the language model.
        """
        response = requests.post(
            self.API_URL,
            headers={"Authorization": f"Bearer {self.API_KEY}"},
            json={"inputs": payload, "parameters": self.parameters},
        )
        if response.status_code == 500:
            raise Response500Exception(self.__str__())

        data = response.json()
        if type(data) == dict and "error" in data.keys():
            raise LanguageModelAPIOverloadException(self.__str__())
        return data[0]["generated_text"].split(payload)[1]

    def preprocess_prompt(self, prompt: str) -> str:
        """
        Preprocess the prompt to be used by the language model.

        BLOOM 176b huggingface.co API have a context window set to 1000 tokens.
        If the prompt is longer than 1000 tokens, it will be truncated.

        :param prompt: The prompt to preprocess.
        :return: The preprocessed prompt.
        """
        tokenized = self.tokenizer(prompt)["input_ids"]
        prompt_len = len(tokenized)
        if prompt_len > 1000:
            return self.tokenizer.decode(tokenized[-1000:])
        return prompt

    def __str__(self) -> str:
        return "BLOOM 176b huggingface.co API"
