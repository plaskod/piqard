import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from piqard.extensions.self_aware.self_ask_loader import SelfAskLoader

import os
os.environ["COHERE_API_KEY"] = "eYDbpsxzTril5NSJTGhv3olRwtNuuAkl9WHK5Vl5"
os.environ["HUGGINGFACE_API_KEY"] = "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"
os.environ["GOOGLE_CUSTOM_SEARCH_API_KEY"] = "AIzaSyAB46rrYmTj6_w-7qCME3Gve7vqcUGzwAY"
os.environ["GOOGLE_CUSTOM_SEARCH_ENGINE_ID"] = "21b53499491814de3"

OPEN_SYSTEM_CONFIG = "./assets/configs/self_ask_config_piqard_piqard.yaml"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/opensystem")
async def opensystem_query(query: Request):
    message = await query.json()
    question = message['question']
    self_ask_loader = SelfAskLoader()
    self_ask = self_ask_loader.load(OPEN_SYSTEM_CONFIG)
    result = self_ask(question)
    result['chain_trace'] = result['chain_trace'].to_json()
    return result

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
