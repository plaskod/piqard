from piqard.context_builders.context_builder import ContextBuilder


class MergedContextBuilder(ContextBuilder):
    @staticmethod
    def build(documents: list[str]) -> str:
        return "\n".join(["- " + " ".join(document.split()[:100]) for document in documents])
