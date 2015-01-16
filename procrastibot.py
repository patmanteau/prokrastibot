# -*- coding: utf-8 -*- 

import requests
import os
import json
import re
from flask import Flask, request
import random
import responder

import config as c

app = Flask(__name__)
app.debug = True

def send_message(text):
	if text != None:
		params = {'token': c.config['access_token']}
		app.logger.debug("sending: {}".format(text))
		payload = {'bot_id': c.config['bot_id'], 'text': text}

		app.logger.debug("payload: {}".format(payload))

		r = requests.post(c.config['bot_url'], params=params, data=json.dumps(payload))
	else:
		app.logger.debug("nothing to send")
		
class Responder:
	def __init__(self, regex, regex_options, func):
		""" Construct a Responder that:
		    1. matches a string against regex using regex_options
		    2. passes matched groups to func
		    3. returns func's result
		"""
		self.regex = regex
		self.regex_options = regex_options
		self.func = func

	def matches(self, string):
		""" Return True if string matches self.regex """
		return bool(re.search(self.regex, string, self.regex_options))

	def respond_to(self, name, text):
		match_obj = re.search(self.regex, text, self.regex_options)
		if match_obj:
			return self.func(name, text, match_obj.groups())

def get_memes():
	memes = {}
	# get memes from imgflip
	memereq = requests.get(c.config['imgflip_get_memes']).json()
	if memereq['success']==True:
		memes = memereq['data']['memes']
	
	return memes


def _prokrast(name, text, groups):
	app.logger.debug("getting link")

	headers = {'User-Agent': 'prokrastibot/1.0'}
	subreddit = "http://www.reddit.com/r/funny/rising.json" if random.randint(1, 10) > 1 else "http://www.reddit.com/r/Motivational/rising.json"
	data = requests.get("http://www.reddit.com/r/funny/rising.json", headers=headers).json()

	i = random.randint(0, len(data['data']['children'])-1)

	title = data['data']['children'][i]['data']['title']
	url = data['data']['children'][i]['data']['url']

	app.logger.debug("title: {} url: {}".format(title, url))

	return [url, title]


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def _memelist(name, text, groups):
	return "https://dl.dropboxusercontent.com/u/2530719/memelist.html"
	
def _meme(name, text, groups):
	app.logger.debug("meme wanted: {} -- {} -- {}".format(name, text, groups))
	
	meme_id = groups[0].strip().lower().replace(' ', '_') if len(groups) > 0 else None
	line1 = groups[1] if len(groups) > 1 else None
	line2 = groups[2] if len(groups) > 2 else None
	
	app.logger.debug("doing meme: {} -- {} -- {}".format(meme_id, line1, line2))
	
	if meme_id:
		#memes = get_memes()
		if meme_id in c.known_memes:
			params = {
				'template_id': c.known_memes[meme_id],
				'username': c.config['imgflip_username'],
				'password': c.config['imgflip_password']
			}
			if line1:
				params['text0'] = line1
			if line2:
				params['text1'] = line2

			app.logger.debug("requesting meme with params: {}".format(str(params)))

			req = requests.post(c.config['imgflip_caption_image'], params=params).json()

			app.logger.debug("resulting request: {}".format(req))
			if req['success']:
				return req['data']['url']
	return None

def _help(name, text, groups):
	return [
		"!memelist: Bekannte Memes",
		"!meme <id>|text0|text1: Erzeugt das Meme <id> mit den angegebenen Texten. Die | sind mandatorisch, auch wenn nur text0 übergeben werden soll."
	]

def _y_u_no(name, text, groups):
	meme_id = c.known_memes['y_u_no']
	line1 = groups[0] if len(groups) > 0 else None
	line2 = groups[1] if len(groups) > 1 else None

	params = {
		'template_id': meme_id,
		'username': c.config['imgflip_username'],
		'password': c.config['imgflip_password']
	}
	if line1:
		params['text0'] = line1
	if line2:
		params['text1'] = line2

	req = requests.post(c.config['imgflip_caption_image'], params=params).json()
	if req['success']:
		return req['data']['url']

class Dispatcher:
	def __init__(self):
		self.registered = []

		self.register(Responder('^!help',
								re.I,
								_help))
		
		self.register(Responder('^!memelist',
								re.I,
								_memelist))
		
		self.register(Responder('^!meme (.+)\|(.+)\|(.*)',
								re.I,
								_meme))
		
		self.register(Responder('^(y u no) (.+)',
								re.I,
								_y_u_no))
		
		self.register(Responder('prokrast',
								re.I,
								_prokrast))
		
		self.register(Responder('^awesome',
								re.I,
								lambda name, text, groups:
									"http://ownyourawesome.files.wordpress.com/2012/09/awesome-meter.jpg"))
		
		self.register(Responder('kann[\w ]*nicht', 
								re.I, 
								lambda name, text, groups:
									"kann-nicht wohnt in der will-nicht-straße, {}".format(name)))

	def register(self, responder):
		self.registered.append(responder)

			
	def answer(self, name, text):
		for r in self.registered:
			if r.matches(text):
				return r.respond_to(name, text)
	
@app.route('/')
def hello():
	app.logger.debug("default route hit")
	return 'OK'

@app.route('/ping', methods=['GET', 'POST'])
def ping():
	message = request.get_json(force=True)
	app.logger.debug("message received: {}".format(str(message)))

	sender = message['name']
	text = message['text']
	app.logger.debug("sender: {} text: {}".format(sender, text))

	resp = Dispatcher()
	answer = resp.answer(sender, text)
	app.logger.debug("will send: {}".format(answer))

	if type(answer) is list:
		app.logger.debug("as list")
		for line in answer:
			send_message(line)
	else:
		app.logger.debug("as single message")
		send_message(answer)

	
	return 'ok'
