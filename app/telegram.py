# python imports
import os
import time
import httpx
from dotenv import load_dotenv
from common import LOGGER

# loading the environment variables
load_dotenv()

TELEGRAM_BOT_SECRET_KEY = os.getenv('TELEGRAM_BOT_SECRET_KEY')
POLLING_INTERVAL = int(os.getenv('POLLING_INTERVAL'))

TELEGRAM_UPDATES_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_SECRET_KEY}/getUpdates'


class TelegramMessage:
    """
    class representation of telegram message
    """
    def __init__(self, text):
      self.text = text

    @property
    def text_lines(self):
        # split lines with line break
        return self.text.split('\n', 1)

    @property
    def task_name(self):
        # first line of message is task name
        LOGGER.warning(f'Task Name: {self.text_lines[0]}')
        return self.text_lines[0]

    @property
    def task_desc(self):
        # second line is the desciption of the text
        if len(self.text_lines) == 2:
            desc = self.text_lines[1]
        else:
            desc = ''
        LOGGER.warning(f'Description: {desc}')
        return desc

    @property
    def hashtags(self):
        # get the last line of description
        last_line = self.task_desc.split('\n')[-1 ] if self.task_desc else ''
        # return hashtags if last line contains only hashtags
        if only_hashtags(last_line):
            hashtags = extract_hash_tags(self.task_desc)
        else:
            hashtags = []
        LOGGER.warning(f'Hashtags are : {hashtags}')
        return hashtags

    @property
    def task_epic(self):
        # first hashtag is the epic name
        LOGGER.warning('Hashtags are: {}'.format(self.hashtags))
        if self.hashtags:
            epic = self.hashtags[0]
        else:
            epic = ''
        LOGGER.warning(f'EPIC: {epic}')
        return epic

    @property
    def task_components(self):
        # leaving the first hashtags others are task components
        if self.hashtags:
          components = self.hashtags[1:]
        else:
            components = []
        LOGGER.warning(f'Components: {components}')
        return components



class TelegramResponse:
    """
    class representation of telegram api response
    """
    def __init__(self, response):
        self.response = response


    @property
    def messages(self):
        message_list = []
        results = self.response.get('result', [])
        for result in results:
          message_list.append(TelegramMessage(result.get('message', {}).get('text')))
        return message_list


def extract_hash_tags(s):
    # return the list of hashtags present in the text
    return [part[1:] for part in s.split() if part.startswith('#')]

def only_hashtags(s):
    # method to check if a string contains only hashtags
    only_hashtags = True
    for part in s.split():
        if part.startswith('#'):
            continue
        else:
            only_hashtags = False
            break
    return only_hashtags

def get_last_message_update_id():
    # get last message update_id on script startup
    params = {'limit': 1}
    r = httpx.get(TELEGRAM_UPDATES_API, params=params)
    if r.status_code == 200:
        telegram_response = r.json()
        latest_update = telegram_response.get('result', [])[0]\
            if telegram_response.get('result', []) else {}
        update_id = latest_update.get('update_id', None)
    else:
        update_id = None
    LOGGER.warning(f'Last Message Update ID {update_id}')
    return update_id

def get_latest_message_update_id(telegram_respone):
    # get update_id of latest message from telergam response
    latest_update = telegram_response.get('result', [])[-1]\
            if telegram_response.get('result', []) else {}
    update_id = latest_update.get('update_id')
    return update_id

def get_latest_updates(update_id=None):
    # fetch latest messages from telegram
    if update_id:
        params = {'offset': update_id}
        r = httpx.get(TELEGRAM_UPDATES_API, params=params)
    else:
        r = httpx.get(TELEGRAM_UPDATES_API)

    if r.status_code == 200:
        telegram_response = r.json()
    else:
        telegram_response = {}

    LOGGER.warning(f'Latest Updates from telegram {telegram_response}')
    return telegram_response

def parse_messages(telegram_response):
    # generate telegram message objects using telegram response
    telegram_response = TelegramResponse(telegram_response)
    telegram_messages = telegram_response.messages
    return telegram_messages



if __name__ == "__main__":

    latest_message_update_id = get_last_message_update_id()
    while True:
        telegram_response = get_latest_updates(latest_message_update_id)
        telegram_messages = parse_messages(telegram_response)
        for message in telegram_messages:
            payload = {
                'name' : message.task_name,
                'desc': message.task_desc,
                'epic': message.task_epic,
                'components': message.task_components
            }

            LOGGER.warning(f'Calling FASTAPI URL: {payload}')
            r = httpx.post('http://localhost:8000/create_jira_task/',
                           json=payload)
            LOGGER.warning(f'Response: {r.text}')

        if get_latest_message_update_id(telegram_response):
            latest_message_update_id = \
                get_latest_message_update_id(telegram_response) + 1

        LOGGER.warning(f'Lastest Message Update ID {latest_message_update_id}')

        # wait for next messages
        time.sleep(POLLING_INTERVAL)
