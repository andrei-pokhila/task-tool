# python imports
import os
from typing import Optional, List
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx

# loading the environment variables
load_dotenv()

app = FastAPI()

JIRA_ISSUE_API = 'https://andrei-pokhila.atlassian.net/rest/api/2/issue/'
JIRA_PROJECT = os.getenv('JIRA_PROJECT_KEY')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')



class JiraTask(BaseModel):
    name: str
    description: Optional[str] = None
    epic: Optional[str] = ''
    components: Optional[List[str]] = []


app = FastAPI()


@app.post("/create_jira_task/")
def create_jira_task(jira_task_payload: JiraTask):
    payload = {
            "fields": {
                "project":
                    {
                        "key": JIRA_PROJECT
                    },
                "summary": jira_task_payload.name,
                "description": jira_task_payload.description,
                   "issuetype": {
                        "name": "Task"
                    }
                }
            }
    r = httpx.post(JIRA_ISSUE_API, json=payload, auth=(JIRA_EMAIL,
                                                       JIRA_PASSWORD))


    return r.json()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
