import os

import ruamel.yaml

from piqard.PIQARD import PIQARD
from piqard.information_retrievers.google_custom_search import GoogleCustomSearch
from piqard.information_retrievers.ranking_retriever import RankingRetriever
from piqard.information_retrievers.vector_retirever import VectorRetriever
from piqard.information_retrievers.annoy_retriver import AnnoyRetriever
from piqard.language_models.bloom_176b_api import BLOOM176bAPI
from piqard.language_models.cohere_api import CohereAPI
from piqard.language_models.gpt_j6b_api import GPTj6bAPI
from piqard.utils.prompt_template import PromptTemplate


class PIQARDLoader:
    def __init__(self):
        self.yaml = ruamel.yaml.YAML()
        self.yaml.register_class(RankingRetriever)
        self.yaml.register_class(VectorRetriever)
        self.yaml.register_class(AnnoyRetriever)
        self.yaml.register_class(GoogleCustomSearch)
        self.yaml.register_class(BLOOM176bAPI)
        self.yaml.register_class(GPTj6bAPI)
        self.yaml.register_class(CohereAPI)
        self.yaml.register_class(PromptTemplate)

    def load(self, config: str) -> PIQARD:
        if os.path.isfile(config):
            with open(config, "r") as f:
                return PIQARD(**self.yaml.load(f))
        else:
            return PIQARD(**self.yaml.load(config))
