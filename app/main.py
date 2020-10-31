# python imports
import os

# 3rd party modules
from fastapi import FastAPI
from dotenv import load_dotenv

# loading the environment variables
load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
