import re
import requests
import random

class Responder:
	def answer(self, name, text):
		return ""

class RegexResponder(Responder):
	def get_random_reddit_link(self):
		data = requests.get("http://www.reddit.com/r/funny/hot.json").json()

		i = random.randint(0, len(data['data']['children'])-1)

		title = data['data']['children'][i]['data']['title']
		url = data['data']['children'][i]['data']['url']
		return (title, url)

	def answer(self, name, text):
		if (re.search('prokrast', text, re.I)):
			(title, url) = self.get_random_reddit_link()
			return [url, title]
		if (re.search('kann[\w ]*nicht', text, re.I)):
			return ["kann-nicht wohnt in der will-nicht-straße, {}".format(name)]
	