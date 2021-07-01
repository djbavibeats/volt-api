import slack_sdk
import os
import json
from pathlib import Path
from flask import Flask, request, Response
from dotenv import dotenv_values
from slackeventsapi import SlackEventAdapter

config = dotenv_values(".env")

app = Flask(__name__)
# slack_event_adapter = SlackEventAdapter(config["SLACK_SECRET"],'/slack/events',app)
slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SECRET"],'/slack/events',app)

# client = slack_sdk.WebClient(token=config["SLACK_TOKEN"])
client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])

BOT_ID = client.api_call('auth.test')['user_id']

print(config)

@app.route('/')
def warning():
    return "<div style='text-align: center; margin: 0 auto;'><img src='https://www.dropbox.com/s/ogtx35aiia317ye/steve%21.jpg?dl=0' /><h3>you shouldn't be here...</h3></div>"

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
    app.run(host='0.0.0.0', port=port)