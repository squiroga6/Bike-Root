# test.py
import sys
import certifi
import ssl

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Verify it works
from slack_sdk import WebClient
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = WebClient(ssl=ssl_context)
api_response = client.api_test()
