from piqard.utils.yaml_constructor import yaml_constructor


@yaml_constructor
class ContextBuilder:
    @staticmethod
    def build(documents: list[str]) -> str:
        pass

    def __str__(self):
        return self.__class__.__name__
