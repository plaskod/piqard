from typing import Optional


class Prompt:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def generate(self, question: str, documents: Optional[list[str]]) -> str:
        pass

    def __str__(self) -> str:
        pass
    