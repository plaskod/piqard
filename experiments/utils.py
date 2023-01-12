import json
import os


def set_env_variables():
    with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
        config = json.load(f)
        os.environ["COHERE_API_KEY"] = config["COHERE_API_KEY"]
        os.environ["HUGGINGFACE_API_KEY"] = config["HUGGINGFACE_API_KEY"]
        os.environ["GOOGLE_CUSTOM_SEARCH_API_KEY"] = config[
            "GOOGLE_CUSTOM_SEARCH_API_KEY"
        ]
        os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"] = config[
            "GOOGLE_CUSTOM_SEARCH_ENGINE_ID"
        ]
