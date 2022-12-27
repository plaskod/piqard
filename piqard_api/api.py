import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import os
import sys
import inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import config
from api_utils import prepare_config_components, yaml_config_from_dict
from piqard.PIQARD_loader import PIQARDLoader
from piqard.extensions.self_ask.self_ask_loader import SelfAskLoader




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/basic_query")
async def basic_query(query: Request):
    message = await query.json()
    question = message['question']
    piqard_yaml_config = yaml_config_from_dict(message)
    piqard_loader = PIQARDLoader()
    piqard = piqard_loader.load(piqard_yaml_config)
    result = piqard(question)
    return {"answer": result["answer"], "context": result["context"]}


@app.post("/benchmark_query")
async def benchmark_query(query: Request):
    pass


@app.get("/get_config_components")
async def get_config_components():
    conifg_components = prepare_config_components()
    return conifg_components


@app.post("/get_prompt_template")
async def get_prompt_template(query: Request):
    message = await query.json()
    template_name = message['template_name']
    with open(f"{config.PROMPTING_TEMPLATES_DIR}\\{template_name}", "r") as f:
        template = f.read()
    return {"template": template}


@app.post("/opensystem")
async def opensystem_query(query: Request):
    message = await query.json()
    question = message['question']
    self_ask_loader = SelfAskLoader()
    self_ask = self_ask_loader.load(f"{config.OPEN_SYSTEM_CONFIG}")
    result = self_ask(question)
    return result

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
