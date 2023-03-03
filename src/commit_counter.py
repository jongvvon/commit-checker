import os
from dotenv import load_dotenv
import requests
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import json
import urllib.request
from PIL import Image

# time = datetime.now()
time = datetime.now() + timedelta(days=1)
date = time.strftime("%Y-%m-%d")
profile_path = 'C:/dev/commit_checker/ref/data.json'


def commit_counter(url):
    req = requests.request("GET", url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    block = soup.find('rect', {"data-date":date})
    commit_count = block.get('data-level')

    return commit_count


def slack_chat(name):
    load_dotenv()
    # ID of the channel you want to send the message to
    channel_id = os.getenv("CHANNEL_ID")
    token = os.getenv("SLACK_TOKEN")

    client = WebClient(token)
    try:
        am_image = client.chat_postMessage(
            text=f"{name}아 커밋해야지?",
            channel=channel_id,
        )
        print("Posting message success")

    except SlackApiError as e:
        print(f"Error posting message: {e}")


if __name__ == '__main__':
    data = open(profile_path, encoding='utf-8')
    profile = json.load(data)

    for data in profile['member']:
        url = data['url']
        img_url = data['img_url']
        if commit_counter(url) == '0':
            slack_chat(data['name'])