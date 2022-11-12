from context_builders.context_builder import ContextBuilder


class TruncatedContextBuilder(ContextBuilder):
    @staticmethod
    def build(documents: list[str]) -> str:
        return " ".join(documents[0].split()[:100])