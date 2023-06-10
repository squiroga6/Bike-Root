import slack_sdk as slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import certifi
import ssl

app = Flask(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Create a slack_event_adapter instance. 
# It will handle events from the Slack API, 
# using the SLACK_SIGNING_SECRET environment variable to authenticate requests.
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'],
                                        '/slack/events', app)


# Create a WebClient instance that will send messages 
# to the Slack API. Make an API call to retrieve the bot's ID.
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context)
BOT_ID = client.api_call("auth.test")['user_id']

onboard_url = "https://drive.google.com/file/d/1lWYhXmqB1V_-HW-gw94Q7FhZ90HPWAUz/view?usp=drive_link"

welcomed_users = set()

# Set up an event listener. It will listen to the member_joined_channel event.
@slack_event_adapter.on('member_joined_channel')
def handle_member_joined_channel(event_data):
    user_id = event_data['event']['user']
    channel_id = event_data['event']['channel']

    # Only send a welcome message if the user is new
    if user_id not in welcomed_users:
        welcomed_users.add(user_id)

        user_info = client.users_info(user=user_id)
        user_name = user_info['user']['name']

        channel_info = client.conversations_info(channel=channel_id)
        channel_name = channel_info['channel']['name']

        if channel_name == 'general':

            greeting = f"""
            Hello {user_name}, welcome to the Bike Root's Slack Channel! We're excited to have you here.
            \nYou can find more information about us at bikeroot.ca . There, you will find our latest schedule. 
            Please note that we are a volunteer-run community bike shop, and therefore our shop is open whenever our volunteers are avaiable. 
            """                     

        elif channel_name == 'volunteer_chat':

            greeting = f"""
            Hello {user_name}, welcome to Bike Root's Volunteer Channel!
            \nThis is a private channel for Bike Root volunteers. Please review our onboarding guide through the link below:
            \n{onboard_url}
            """

        else:

            greeting = f"""
            Hello {user_name}, welcome to the {channel_name} "channel! We're excited to have you here.
            """

        client.chat_postMessage(channel=channel_id, text=greeting)

if __name__ == "__main__":
    app.run(debug=True, port=5000)        
