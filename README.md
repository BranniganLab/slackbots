# slackbots
Various bots intended to be integrated with slack 

How to Build a Slackbot with Python + Flask

This guide will help you build and deploy a Slackbot using Python, Flask, and either your local machine (with ngrok) or PythonAnywhere. It assumes basic comfort with Python but no prior experience with Slack app development.

# 1. Create a Slack App

Go to https://api.slack.com/apps

Click "Create New App" > "From scratch"

Give your app a name (e.g. MyBot) and select your Slack workspace

# 2. Add a Slash Command

In the left menu, click Slash Commands

Click Create New Command

Command: /mybot

Request URL: (see below: PythonAnywhere or ngrok URL)

Short Description: A test bot

Usage Hint: name=value name2=value2

Save the command

# 3. Enable Interactivity (Optional for buttons or modals)

In the left menu, click Interactivity & Shortcuts

Turn it ON

Set the Request URL to the same endpoint as the slash command

# 4. Install the App to Your Workspace

In the left menu, click OAuth & Permissions

Click Install App to Workspace

Authorize

# 5. Write Your Flask App

Here is a minimal example (app.py):

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def respond():
    user_input = request.form.get("text", "")
    return jsonify({
        "response_type": "in_channel",
        "text": f"You said: {user_input}"
    })

if __name__ == "__main__":
    app.run()

# 6A. Deploy Locally with ngrok (for testing)

Install ngrok

In terminal:

ngrok http 5000

Copy the URL (e.g. https://abcd1234.ngrok.io) into Slack as the Request URL

Run your app with python app.py

# 6B. Deploy with PythonAnywhere (for persistent hosting)

Create an account

Go to the Files tab, upload your app.py

Go to the Web tab, create a new web app (Manual, Python 3.x)

In the WSGI file, point to your app:

import sys
path = "/home/yourusername"
if path not in sys.path:
    sys.path.append(path)
from app import app as application

Reload the app

Use https://yourusername.pythonanywhere.com/slack/command as your Slack Request URL

# 7. Test It

In Slack:

/mybot Hello world

You should get a response: You said: Hello world
