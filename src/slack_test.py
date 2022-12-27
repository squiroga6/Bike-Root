import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

os.environ["ENV_VAR"] = "default"
from set_params import *

client = WebClient(token=SLACK_BOT_TOKEN)
client.chat_postMessage(channel=CHANNEL_ID, 
                        text="Hello world!")