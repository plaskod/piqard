class DynamicPromptingNotImplementedException(Exception):
    def __init__(
        self, information_retriever: str, message="Dynamic prompting not implemented"
    ):
        self.information_retriever = information_retriever
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.information_retriever} -> {self.message}"
