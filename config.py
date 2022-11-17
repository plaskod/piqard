from context_builders.merged_context_builder import MergedContextBuilder
from context_builders.truncated_context_builder import TruncatedContextBuilder
from information_retrieval.ranking_retriever.ranking_retriever import RankingRetriever
from information_retrieval.vector_retriever.vector_retirever import VectorRetriever
from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI


result_dir = "result"


class PIQARDConfig:
    information_retriever = None
    large_language_model = BLOOM176bAPI()
    prompt_template = "prompting/templates/context_prompt.txt"
    context_builder = TruncatedContextBuilder()
