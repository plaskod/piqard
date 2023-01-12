class DynamicPromptingNotImplementedException(Exception):
    def __init__(
        self, information_retriever: str, message="Dynamic prompting not implemented"
    ):
        self.information_retriever = information_retriever
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.information_retriever} -> {self.message}"


class Response500Exception(Exception):
    def __init__(self, language_model: str, message="Response 500 exception"):
        self.language_model = language_model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"\n{self.language_model} -> {self.message}"


class LanguageModelAPIOverloadException(Exception):
    def __init__(self, language_model: str, message="API key hourly ratio exceeded."):
        self.language_model = language_model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"\n{self.language_model} -> {self.message}"


class LanguageModelAPILockedOutput(Exception):
    def __init__(self, language_model: str, message="Locked output"):
        self.language_model = language_model
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"\n{self.language_model} -> {self.message}"


class EnvironmentVariableNotSet(Exception):
    def __init__(self, env_variable: str, message="Environment variable is not set"):
        self.env_variable = env_variable
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"\n{self.env_variable} -> {self.message}"
