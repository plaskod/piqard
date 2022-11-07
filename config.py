from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.prompt import Prompt

result_dir = "result"


class PIQARDConfig:
    information_retriever = GoogleCustomSearch()
    large_language_model = BLOOM176bAPI()
    prompt_generator = Prompt("prompting/templates/5_shot_prompt.yaml")
