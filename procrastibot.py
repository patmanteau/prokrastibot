# -*- coding: utf-8 -*- 

import requests
import os
import json
import re
from flask import Flask, request
import random

import config as c

app = Flask(__name__)
app.debug = True

running_local=False

def send_message(text):
	params = {'token': c.config['access_token']}
	
	if (not running_local):
		payload = {'bot_id': c.config['bot_id'], 'text': text}
		r = requests.post(c.config['bot_url'], params=params, data=json.dumps(payload))
		app.logger.debug("send -> {}".format(text))
	else:
		app.logger.debug("send -> {}".format(text))
		

def get_random_reddit_link():
	data = requests.get("http://www.reddit.com/r/funny/hot.json").json()

	i = random.randint(0, len(data['data']['children'])-1)

	title = data['data']['children'][i]['data']['title']
	url = data['data']['children'][i]['data']['url']
	return (title, url)

def process(message):
	sender = message['name']
	text = message['text']
	
	if (re.search('prokrast', text, re.I)):
		(title, url) = get_random_reddit_link()
		send_message(url)
		send_message(title)
		
	elif (re.search('kann[\w ]*nicht', text, re.I)):
		send_message("kann-nicht wohnt in der will-nicht-straße, {}".format(name))
	

@app.route('/')
def hello():
	return 'OK'

@app.route('/ping', methods=['GET', 'POST'])
def ping():
	process(request.get_json(force=True))
	
	return 'ok'
