from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class LanguageModel:
    def query(self, payload: str) -> str:
        pass

    def __str__(self):
        return self.__class__.__name__


class LanguageModelAPIOverloadException(Exception):
    pass
