import slack_sdk
import os
import json
from pathlib import Path
from flask import Flask, request, Response
from dotenv import dotenv_values, load_dotenv
from slackeventsapi import SlackEventAdapter

load_dotenv()
config = dotenv_values(".env")

app = Flask(__name__)

if os.environ["PRODUCTION"] == True:
    slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SECRET"],'/slack/events',app)
    client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])
    host = '0.0.0.0'
else:
    slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SECRET"],'/slack/events',app)
    client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])
    host = '127.0.0.1'

BOT_ID = client.api_call('auth.test')['user_id']

print(config)

@app.route('/')
def warning():
    return "<div style='overflow: hidden; height: 100vh; display: flex; flex-direction: column; justify-content: center; text-align: center; margin: 0 auto;'><img style='width: 65%; margin: 0 auto;' src='https://previews.dropbox.com/p/thumb/ABNkfTnO0XCrAYYpqQ4dVxhaqordD1In-fbI7tx_MNOgeB-ILyt9r-hcuMgKX4hR9KLsMG9XA870e2zqJxZmUOAa9ecWd_ZqsePJCsf5FRspiU-iHDQQph3XEF2R9lrK4VpWEBSAq7eAtdYPyIeJovFBtKlBiqhddBUpsyPLjcBYNS8tDHNj-k-YX9BXePgG4O433cMeoUDMhG3kihcc1IvdiXZjI7qTJ5XNgdz-VChCzCVY8OxZlK0-Qdu9v7uTUfJA4RvhGB2dKMuvphYF8qMlnCDD3DIiZviojCatW-CKlc5zTw3aE5mAX3J2uwXbjCobNK3tX8L5Jqp23EJiEL4gRTmrZi0cEs2svHIJ7MW6Aw/p.jpeg?fv_content=true&size_mode=5' /><h1>you shouldn't be here...</h1></div>"

@app.route("/send-message", methods=['POST'])
def send_message():
    json_data = json.loads(str(request.data, encoding='utf-8'))
    channel = json_data["channel"]
    text = json_data["text"]
    client.chat_postMessage(channel=channel, text=text)
    return Response(), 200

@app.route("/yell-at-me", methods=['POST'])
def yell_at_me():
    data = request.form
    print(data)
    user = data["user_name"]
    userId = data["user_id"]
    channel = data["channel_name"]
    text = "HEY, " + user.upper() + ", GET BENT"
    client.chat_postMessage(channel=userId, text=text)
    return Response(), 200

if (__name__ == "__main__"):
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)