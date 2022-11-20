import os

import ruamel.yaml
from piqard.PIQARD import PIQARD
from piqard.context_builders.merged_context_builder import MergedContextBuilder
from piqard.context_builders.truncated_context_builder import TruncatedContextBuilder
from piqard.information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from piqard.information_retrieval.ranking_retriever import RankingRetriever
from piqard.information_retrieval.vector_retirever import VectorRetriever
from piqard.language_models.bloom_176b_api import BLOOM176bAPI
from piqard.language_models.gpt_j6b_api import GPTj6bAPI
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
        if os.path.isfile(path):
            with open(path, "r") as f:
                return PIQARDConfig(**self.yaml.load(f))
        else:
            return PIQARDConfig(**self.yaml.load(path))
