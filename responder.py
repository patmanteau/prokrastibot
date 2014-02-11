import os
import re
import requests
import json
import random
import config

class Responder:
	def answer(self, name, text):
		return ""

class RegexResponder(Responder):
	def get_random_reddit_link(self):
		data = requests.get("http://www.reddit.com/r/funny/rising.json").json()

		i = random.randint(0, len(data['data']['children'])-1)

		title = data['data']['children'][i]['data']['title']
		url = data['data']['children'][i]['data']['url']
		return (title, url)

	def get_memes(self):
		memes = {}
		# get memes from imgflip
		memereq = requests.get(config.config['imgflip_get_memes']).json()
		if memereq['success']==True:
			for meme in memereq['data']['memes']:
				memes[meme['id']] = meme['name']
		
		return memes

	def answer_memelist(self, name, text):
		# get memes from imgflip
		memes = self.get_memes()
		memelist = []
		for k, v in memes.items():
			memelist.append('"{name}" -> {id}'.format(name=v, id=k))
		
		if len(memelist) > 0:
			return '@{name}, zur Auswahl:\n'.format(name=name) + '\n'.join(sorted(memelist))
		else:
			return None
		

	def answer_meme(self, name, text):
		cmdline = text.strip().split('|')
		
		meme_id = cmdline[0] if len(cmdline) > 0 else None
		line1 = cmdline[1] if len(cmdline) > 1 else None
		line2 = cmdline[2] if len(cmdline) > 2 else None

		print(meme_id)
		print(line1) 
		print(line2)

		if meme_id:
			memes = self.get_memes()
			if meme_id in memes:
				params = {
					'template_id': meme_id,
					'username': config.config['imgflip_username'],
					'password': config.config['imgflip_password']
				}
				if line1:
					params['text0'] = line1
				if line2:
					params['text1'] = line2

				req = requests.post(config.config['imgflip_caption_image'], params=params).json()
				if req['success']:
					return req['data']['url']
		return None
		
	def answer(self, name, text):
		if text.startswith('!memelist'):
			return [self.answer_memelist(name, text[5:])]
		elif text.startswith('!meme'):
			return [self.answer_meme(name, text[5:])]
		elif (re.search('prokrast', text, re.I)):
			(title, url) = self.get_random_reddit_link()
			return [url, title]
		elif (re.search('kann[\w ]*nicht', text, re.I)):
			return ["kann-nicht wohnt in der will-nicht-straße, {}".format(name)]
	