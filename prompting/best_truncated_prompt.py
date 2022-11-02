from typing import Optional
from prompting.prompt import Prompt


prompt = "Question: {question}\nContext: {context}\nAnswer:"


class BestTruncatedPrompt(Prompt):
    def __init__(self):
        super().__init__(prompt)

    def generate(self, question: str, documents: Optional[list]) -> str:
        first_512_words = " ".join(documents[0]['text'].split()[:512])
        return self.prompt.format(question=question, context=first_512_words)

    def __str__(self):
        return "Best of retrieved documents truncated to 512 words."
