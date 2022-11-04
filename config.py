from information_retrieval.google_custom_search.gcs import GoogleCustomSearch
from large_language_models.bloom_176b_api.bloom_176b_api import BLOOM176bAPI
from large_language_models.gpt_j6b_api.gpt_j6b_api import GPTj6bAPI
from prompting.basic_prompt import BasicPrompt
from prompting.best_truncated_prompt import BestTruncatedPrompt
from prompting.few_shot_prompt import ZeroShotUserEngagementPrompt, FewShotUserEngagmentPrompt

result_dir = "result"

class PIQARDConfig:
    large_language_model = BLOOM176bAPI()
    prompt_generator = FewShotUserEngagmentPrompt()
