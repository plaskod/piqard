class BasicPrompt:
    def __init__(self):
        self.prompt = "Question: {}\nAnswer:"

    def generate(self, question: str) -> str:
        return self.prompt.format(question)
