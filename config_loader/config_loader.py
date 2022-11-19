import ruamel.yaml
from PIQARD import PIQARD
from context_builders.merged_context_builder import MergedContextBuilder
from context_builders.truncated_context_builder import TruncatedContextBuilder
from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from information_retrieval.ranking_retriever.ranking_retriever import RankingRetriever
from information_retrieval.vector_retriever.vector_retirever import VectorRetriever
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.prompt_generator import PromptGenerator


class PIQARDConfig:
    def __init__(
        self, piqard: PIQARD, result_dir: str = "result", benchmark: str = None
    ):
        self.piqard = piqard
        self.result_dir = result_dir
        self.benchmark = benchmark


class ConfigLoader:
    def __init__(self):
        self.yaml = ruamel.yaml.YAML()
        self.yaml.register_class(PIQARD)
        self.yaml.register_class(RankingRetriever)
        self.yaml.register_class(VectorRetriever)
        self.yaml.register_class(GoogleCustomSearch)
        self.yaml.register_class(PromptGenerator)
        self.yaml.register_class(TruncatedContextBuilder)
        self.yaml.register_class(MergedContextBuilder)
        self.yaml.register_class(BLOOM176bAPI)
        self.yaml.register_class(GPTj6bAPI)

    def load(self, path: str) -> PIQARDConfig:
        with open(path, "r") as f:
            return PIQARDConfig(**self.yaml.load(f))
