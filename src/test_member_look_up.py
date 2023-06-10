import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from src.download_memberships import download_memberships
from src.utils import member_stats, member_search

os.environ["ENV_VAR"] = "default"
from set_params import *

members = download_memberships()

stats = member_stats(members)

import re
command = "Search for: quiroga"
name = re.findall(pattern="(?<=:).*",string=command)[0].strip()
member_info = member_search(members,name)