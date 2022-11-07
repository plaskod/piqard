from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.basic_prompt import BasicPrompt
from prompting.best_truncated_prompt import BestTruncatedPrompt
from prompting.few_shot_prompt import FewShowPrompt
from prompting.few_shot_prompt_RealTimeQA import FewShowPromptRealTimeQA

result_dir = "result"


class PIQARDConfig:
    information_retriever = None
    large_language_model = BLOOM176bAPI()
    prompt_generator = FewShowPromptRealTimeQA()
