from typing import Optional
from prompting.prompt import Prompt


prompt = "Question: {}\nAnswer:"


class BasicPrompt(Prompt):
    def __init__(self):
        super().__init__(prompt)

    def generate(self, question: str, documents: Optional[list[str]]) -> str:
        return self.prompt.format(question)

    def __str__(self):
        return "Basic question - answer"
