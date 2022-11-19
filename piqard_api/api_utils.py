import glob

from piqard_api import config


def get_config_components() -> dict:
    prompting_templates = [{"name": "custom_prompt", "value": "custom_prompt"}] + [
        {
            "name": prompt.replace(config.PROMPTING_TEMPLATES_DIR, ""),
            "value": prompt.replace(config.PROMPTING_TEMPLATES_DIR, ""),
        }
        for prompt in glob.glob(f"{config.PROMPTING_TEMPLATES_DIR}\\**\\*.txt", recursive=True)
    ]
    return {
        "information_retriever": [
            {"name": "GoogleCustomSearch", "value": "!GoogleCustomSearch"},
            {"name": "RankingRetriever", "value": "!RankingRetriever"},
            {"name": "VectorRetriever", "value": "!VectorRetriever"},
        ],
        "prompt_template": prompting_templates,
        "context_builder": [
            {"name": "TruncatedContext", "value": "!TruncatedContext"},
            {"name": "MergedContext", "value": "!MergedContext"},
        ],
        "large_language_model": [
            {"name": "BLOOM 176B API", "value": "!BLOOM176bAPI"},
            {"name": "GPT-J6B API", "value": "!GPTj6bAPI"},
        ],
    }
