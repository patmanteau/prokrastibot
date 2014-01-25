import requests
import os
import json
from flask import Flask, request

access_token = "6f657c8067e701314824028b45ba2ff5"
bot_id = "999711d482b0075f6dea2b35e7"
params = { "token": access_token }
group_id = "6870628"
bot_url = "https://api.groupme.com/v3/bots/post"

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
	#payload = { 'bot_id': bot_id,'text': "http://reddit.com/r/pics" }
	#r = requests.post(bot_url, params=params, data=json.dumps(payload))
	return 'OK'

@app.route('/ping')
def ping():
	message = request.form
	print(message)

	#payload = { 'bot_id': bot_id,'text': "http://reddit.com/r/pics" }
	#r = requests.post(bot_url, params=params, data=json.dumps(payload))
	return 'OK'
