from config_loader.yaml_constructor import yaml_constructor


@yaml_constructor
class LanguageModel:
    def query(self, payload: str) -> str:
        pass

    def __str__(self) -> str:
        return "Language Model"
