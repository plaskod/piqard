from config_loader.yaml_constructor import yaml_constructor


@yaml_constructor
class ContextBuilder:
    @staticmethod
    def build(documents: list[str]) -> str:
        pass
