import glob

import jinja2
import config


def prepare_config_components() -> dict:
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
        "k": [
            {"name": "1", "value": 1},
            {"name": "2", "value": 2},
            {"name": "3", "value": 3},
            {"name": "4", "value": 4},
            {"name": "5", "value": 5},
        ],
        "prompt_template": prompting_templates,
        "language_model": [
            {"name": "BLOOM 176B API", "value": "!BLOOM176bAPI"},
            {"name": "GPT-J6B API", "value": "!GPTj6bAPI"},
        ],
    }


def yaml_config_from_dict(message: dict):
    piqard_config_dict = message['piqard']
    if piqard_config_dict['prompt_template'] == "custom_prompt":
        piqard_config_dict['prompt_template'] = message['prompt_template']
    else:
        piqard_config_dict[
            'prompt_template'] = f"{config.PROMPTING_TEMPLATES_DIR}{piqard_config_dict['prompt_template']}".replace(
            "\\", "\\\\")

    environment = jinja2.Environment()
    with open(config.CONFIG_TEMPLATE, "r") as file:
        prompt_template = file.read()
    yaml_config_template = environment.from_string(prompt_template)
    yaml_config = yaml_config_template.render(
        information_retriever=piqard_config_dict['information_retriever'] if piqard_config_dict[
                                                                                 'information_retriever'] not in [
                                                                                 'none', ''] else None,
        database=piqard_config_dict['data_base'] if piqard_config_dict['data_base'] not in ['none', ''] else None,
        k=piqard_config_dict['k'] if piqard_config_dict['k'] not in ['none', ''] else None,
        prompt_template=piqard_config_dict['prompt_template'],
        language_model=piqard_config_dict['language_model'])

    return yaml_config
