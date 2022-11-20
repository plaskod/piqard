import uvicorn
from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from piqard_api.api_utils import get_config_components, process_PIQARD_result_query
from piqard_api import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def PIQARD_basic_query(query: Request):
    message = await query.json()
    print(message['prompt_template'])
    config, question = process_PIQARD_result_query(message)
    result = config.piqard(question)
    print(result)
    return {"answer": result["answer"], "context": result["context"]}


@app.get("/get_config_components")
async def PIQARD_config_components():
    conifg_components = get_config_components()
    return conifg_components


@app.post("/get_prompt_template")
async def get_prompt_template(query: Request):
    message = await query.json()
    print(message)
    template_name = message['template_name']
    with open(f"{config.PROMPTING_TEMPLATES_DIR}\\{template_name}", "r") as f:
        template = f.read()
    print(template)
    return {"template": template}

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
