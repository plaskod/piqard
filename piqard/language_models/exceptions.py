class Response500Exception(Exception):
    def __init__(self, language_model: str, message="Response 500 exception"):
        self.language_model = language_model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'\n{self.language_model} -> {self.message}'

class LanguageModelAPIOverloadException(Exception):
    def __init__(self, language_model: str, message="API key hourly ratio exceeded."):
        self.language_model = language_model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'\n{self.language_model} -> {self.message}'

