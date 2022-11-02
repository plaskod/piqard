class BestTruncatedPrompt:
    def __init__(self):
        self.prompt = "Question: {}\nContext: {}\nAnswer:"

    def generate(self, question: str, context: str) -> str:
        first_512_words = " ".join(context.split()[:512])
        return self.prompt.format(question, first_512_words)
