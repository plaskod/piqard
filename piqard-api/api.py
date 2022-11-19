import uvicorn
from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
import json

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config_loader.config_loader import ConfigLoader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def PIQARD_basic_query(query: Request):
    message = await query.json()
    config_loader = ConfigLoader()
    config = config_loader.load("config_loader/configs/config.yaml")

    piqard = config.piqard
    result = piqard(message['question'])

    print(result)
    return {'answer': result['answer'], 'context': result['context']}


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)
