import os

import ruamel.yaml

from piqard.extensions.react.action import Action
from piqard.extensions.react.agent import Agent
from piqard.information_retrievers.google_custom_search import GoogleCustomSearch
from piqard.information_retrievers.ranking_retriever import RankingRetriever
from piqard.information_retrievers.vector_retirever import VectorRetriever
from piqard.information_retrievers.annoy_retriver import AnnoyRetriever
from piqard.information_retrievers.wiki_api import WikiAPI
from piqard.language_models.bloom_176b_api import BLOOM176bAPI
from piqard.language_models.cohere_api import CohereAPI
from piqard.language_models.gpt_j6b_api import GPTj6bAPI
from piqard.utils.prompt_template import PromptTemplate


class AgentLoader:
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
        self.yaml.register_class(Action)
        self.yaml.register_class(WikiAPI)

    def load(self, config: str) -> Agent:
        if os.path.isfile(config):
            with open(config, "r") as f:
                return Agent(**self.yaml.load(f))
        else:
            return Agent(**self.yaml.load(config))