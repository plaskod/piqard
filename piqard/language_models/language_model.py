from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class LanguageModel:
    def __init__(self, stop_token: str = None):
        self.stop_token = stop_token

    def query(self, payload: str) -> str:
        pass

    def __str__(self):
        return self.__class__.__name__
