# About the project:
Task Tool is an application using which you can create JIRA issues using Telegram messages.

## Setting up environment variables
To run the serice you will need to configure the .env file in the app/ directory.

Create a file called .env(touch .env) and add the following parameters:

`TELEGRAM_BOT_SECRET_KEY=<place you telegram bot key here>`

`POLLING_INTERVAL=10`


`JIRA_EMAIL=<Jira Login email>`

`JIRA_PASSWORD=<Jira API token>`

`JIRA_PROJECT_KEY=<Jira Project Key to use>`

`JIRA_EPIC_CUSTOM_FIELD=<JIRA EPIC URL Customfild ID eg: customfield_10014>`


## Running using Docker:

`docker-compose build`

`docker-compose up`

## Setting up dev:

### Installing Python and dependencies:
Installing Pyenv to manage python versions

[Pyenv](https://github.com/pyenv/pyenv#installation)

Installing Python:

`pyenv install 3.7.3`

Installing Poetry to manage dependencies:

[Poetry](https://python-poetry.org/docs/#installation)

Creating virtualenv:

`pyenv virtualenv 3.7.3 task_tool_venv`

Activating virtualenv:

`pyenv activate task_tool_venv`

Clone the repository then:

`cd app/`

`poetry install`

Running the services:

Activate the virtualenv in both terminals before running the commands

On one terminal run the telegram message reading service(in app/ directory):

`python telegram.py`

This service will keep keep polling for the incoming messages

On the second terminal run the FastAPI service(in app/ directory):

`uvicorn main:app --reload`

Now both services are running independently, now when you send a message to telegram it should create the relevant task.
