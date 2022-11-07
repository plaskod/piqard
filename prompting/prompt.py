from typing import Optional
import yaml


class Prompt:
    def __init__(self, prompt_path: str):
        with open(prompt_path, 'r') as file:
            template = yaml.safe_load(file)
        self.prompt = template['text']
        self.info = template['info']

    def generate(self, question: str, context: Optional[str]) -> str:
        return self.prompt.format(question=question, context=context if context else '')

    def __str__(self) -> str:
        return self.info
