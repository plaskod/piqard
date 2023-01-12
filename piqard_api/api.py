import uvicorn
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from piqard.extensions.self_aware.self_aware_loader import SelfAwareLoader

import os

with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    config = json.load(f)
    os.environ["COHERE_API_KEY"] = config["COHERE_API_KEY"]
    os.environ["HUGGINGFACE_API_KEY"] = config["HUGGINGFACE_API_KEY"]
    os.environ["GOOGLE_CUSTOM_SEARCH_API_KEY"] = config["GOOGLE_CUSTOM_SEARCH_API_KEY"]
    os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"] = config[
        "GOOGLE_CUSTOM_SEARCH_ENGINE_ID"
    ]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/opensystem")
async def opensystem_query(query: Request) -> dict:
    """
    OpenSystem query endpoint
    :param query: query
    :return: response
    """
    message = await query.json()
    question = message["question"]
    self_aware_loader = SelfAwareLoader()
    self_aware = self_aware_loader.load(config["OPEN_SYSTEM_CONFIG"])
    result = self_aware(question)
    result["chain_trace"] = result["chain_trace"].to_json()
    return result


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
