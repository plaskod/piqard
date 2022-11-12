from context_builders.merged_context_builder import MergedContextBuilder
from context_builders.truncated_context_builder import TruncatedContextBuilder
from information_retrieval.vector_retriever.vector_retirever import VectorRetriever
from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.prompt import Prompt


result_dir = "result"


class PIQARDConfig:
    information_retriever = VectorRetriever('test/open_book_qa/openbook.txt',
                                            'test/open_book_qa/index_multi-qa-MiniLM-L6-cos-v1.pickle')
    large_language_model = BLOOM176bAPI()
    prompt_generator = Prompt("prompting/templates/5_shot_openbookqa.yaml")
    context_builder = MergedContextBuilder()
