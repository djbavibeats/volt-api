# import slack_sdk
import os
import json
from pathlib import Path
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_login import login_user, logout_user, current_user
from dotenv import load_dotenv
# from slackeventsapi import SlackEventAdapter
from db.models import User, Project
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect, update

load_dotenv()

from db import create_app

app = create_app()

CORS(app)

if os.environ["PRODUCTION"] == "True":
    # slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SECRET"],'/slack/events',app)
    # client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])
    host = '0.0.0.0'
else:
    # slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SECRET"],'/slack/events',app)
    # client = slack_sdk.WebClient(token=os.environ["SLACK_TOKEN"])
    host = '127.0.0.1'

# BOT_ID = client.api_call('auth.test')['user_id']

print(host)

@app.route('/')
def warning():
    return "<div style='overflow: hidden; height: 100vh; display: flex; flex-direction: column; justify-content: center; text-align: center; margin: 0 auto;'><img style='width: 65%; margin: 0 auto;' src='https://www.dropbox.com/s/ogtx35aiia317ye/steve%21.jpg?raw=0' /><h1>you shouldn't be here...</h1></div>"

# AUTH ROUTES
@app.route("/sign-up", methods=['POST'])
def sign_up():
    data = json.loads(str(request.data, encoding='utf-8'))
    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(
            status= 400,
            message= "User already exists"
        )
    new_user = User(username= username, email=email, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify(
        status= 200,
        message= "Success"
    )

@app.route("/login", methods=['POST'])
def login():
    data = json.loads(str(request.data, encoding='utf-8'))
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            authedUser = User.query.filter_by(username=username).first()
            return jsonify(
                status= 200,
                message= "Success"
            )
        else:
            return jsonify(
                status= 400,
                message= "Incorrect password"
            )
    else:
        return jsonify(
            status= 400,
            message= "User does not exist"
        )

@app.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return
# END AUTH ROUTES

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
                

# USER ROUTES
@app.route("/users/get-by-username", methods=['POST'])
def get_by_username():
    data = json.loads(str(request.data, encoding='utf-8'))
    username= data['username']

    user = User.query.filter_by(username=username).first()

    jsonUser = object_as_dict(user)

    return jsonify(
        id= jsonUser['id'],
        username= jsonUser['username'],
        email= jsonUser['email']
    )
# END USER ROUTES

# PROJECT ROUTES
@app.route("/projects", methods=['GET'])
def get_all_projects():
    # data = json.loads(str(request.data, encoding='utf-8'))
    projects = db.session.query(Project).all()
    jsonProjects = []

    for project in projects:
        jsonProject = object_as_dict(project)
        jsonProjects.append(jsonProject)

    print(jsonProjects)
    return jsonify(
        projects=jsonProjects
    )

@app.route("/projects/create", methods=['POST'])
def create_project():
    data = json.loads(str(request.data, encoding='utf-8'))

    new_project = Project(project_name=data['project_name'], user_id=data['user_id'], domain=data['domain'], hosting=data['hosting'], web_platform=data['web_platform'], description=data['description'])
    db.session.add(new_project)
    db.session.commit()

    jsonProject = object_as_dict(new_project)

    return jsonify(
        jsonProject
    )

@app.route("/projects/get-by-user-id", methods=['POST'])
def get_projects():
    data = json.loads(str(request.data, encoding='utf-8'))

    jsonProjects = []
    projects = db.session.query(Project).all()
    for project in projects:
        if project.user_id == data['user_id']:
            jsonProject = object_as_dict(project)
            jsonProjects.append(jsonProject)


    print(jsonProjects)
    return jsonify(
        projects=jsonProjects
    )

@app.route("/projects/update", methods=['POST'])
def update_project():
    data = json.loads(str(request.data, encoding='utf-8'))

    print(data)
    
    instance = Project.query.filter(Project.id==data['id'])
    info=instance.update(dict(data))
    db.session.commit()
    updateddata=instance.first()
    msg={"msg":"User details updated successfully","data":updateddata.serializers()}
    code=200

    return msg
# END PROJECT ROUTES

# SLACK ROUTES
# @app.route("/send-message", methods=['POST'])
# def send_message():
#     json_data = json.loads(str(request.data, encoding='utf-8'))
#     channel = json_data["channel"]
#     text = json_data["text"]
#     client.chat_postMessage(channel=channel, text=text)
#     return Response({ "nice" }), 200

# @app.route("/yell-at-me", methods=['POST'])
# def yell_at_me():
#     data = request.form

#     user = data["user_name"]
#     userId = data["user_id"]
#     channel = data["channel_name"]
#     text = "HEY, " + user.upper() + ", GET BENT"
#     client.chat_postMessage(channel=userId, text=text)
#     return Response(), 200
# END SLACK ROUTES

if (__name__ == "__main__"):
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)