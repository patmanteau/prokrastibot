import requests
import os
import json
import re
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

@app.route('/ping', methods=['GET', 'POST'])
def ping():
	message = request.get_json(force=True)
	text = message['text']
	name = message['name']

	if (re.search('prokrast', text, re.I)):
		payload = { 'bot_id': bot_id,'text': '@{}: http://reddit.com/r/funny'.format(name) }
		r = requests.post(bot_url, params=params, data=json.dumps(payload))
		payload = { 'bot_id': bot_id,'text': 'komm, du willst es doch auch!!' }
		r = requests.post(bot_url, params=params, data=json.dumps(payload))
		return '@{}: http://reddit.com/r/funny'.format(name)

	return 'OK'
