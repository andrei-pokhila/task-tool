# python imports
import os
from typing import Optional, List
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import httpx
from common import LOGGER
# loading the environment variables
load_dotenv()

app = FastAPI()

JIRA_ISSUE_API = 'https://andrei-pokhila.atlassian.net/rest/api/2/issue/'
JIRA_PROJECT = os.getenv('JIRA_PROJECT_KEY')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
JIRA_EPIC_CUSTOM_FIELD = os.getenv('JIRA_EPIC_CUSTOM_FIELD')


class JiraTask(BaseModel):
    name: str
    desc: Optional[str] = None
    epic: Optional[str] = ''
    components: Optional[List[str]] = []


def get_create_issue_payload(request_data):
    # use request data to create payload for Jira
    payload = {
            "fields": {
                "project":
                    {
                        "key": JIRA_PROJECT
                    },
                "summary": request_data.name,
                "description": request_data.desc,
                   "issuetype": {
                        "name": "Task"
                    },
                'components': [{'name': component} for component in request_data.components],
                JIRA_EPIC_CUSTOM_FIELD: request_data.epic
                }
            }
    LOGGER.warning(f'Jira payload: {payload}')
    return payload


app = FastAPI()


@app.post("/create_jira_task/")
def create_jira_task(jira_task_payload: JiraTask):
    # use the request data to create the issue
    payload = get_create_issue_payload(jira_task_payload)
    r = httpx.post(JIRA_ISSUE_API, json=payload, auth=(JIRA_EMAIL,
                                                       JIRA_PASSWORD))
    return r.json()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
