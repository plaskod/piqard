import glob

import jinja2

from config_loader.config_loader import ConfigLoader
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
            {"name": "None", "value": "none"},
        ],
        "data_base": [
            {"name": "OpenBookQA Facts", "value": "openbookqa"},
        ],
        "prompt_template": prompting_templates,
        "context_builder": [
            {"name": "TruncatedContext", "value": "!TruncatedContextBuilder"},
            {"name": "MergedContext", "value": "!MergedContextBuilder"},
        ],
        "large_language_model": [
            {"name": "BLOOM 176B API", "value": "!BLOOM176bAPI"},
            {"name": "GPT-J6B API", "value": "!GPTj6bAPI"},
        ],
    }


def process_PIQARD_result_query(message: dict):
    piqard_config_dict = message['piqard']
    if piqard_config_dict['prompt_template'] == "custom_prompt":
        piqard_config_dict['prompt_template'] = message['prompt_template']
    else:
        piqard_config_dict[
            'prompt_template'] = f"{config.PROMPTING_TEMPLATES_DIR}{piqard_config_dict['prompt_template']}"

    environment = jinja2.Environment()
    with open(config.CONFIG_TEMPLATE, "r") as file:
        prompt_template = file.read()
    yaml_config_template = environment.from_string(prompt_template)
    yaml_config = yaml_config_template.render(information_retriever=piqard_config_dict['information_retriever'] if piqard_config_dict['information_retriever'] not in ['none', ''] else None,
                                              database=piqard_config_dict['data_base'] if piqard_config_dict['data_base'] not in ['none', ''] else None,
                                              prompt_template=piqard_config_dict['prompt_template'],
                                              context_builder=piqard_config_dict['context_builder'],
                                              large_language_model=piqard_config_dict['large_language_model'])

    config_loader = ConfigLoader()
    final_config = config_loader.load(yaml_config)
    question = message['question']
    return final_config, question
