import os
from flask import Flask

access_token = "6f657c8067e701314824028b45ba2ff5"
bot_id = "999711d482b0075f6dea2b35e7"
params = { "token": access_token }
group_id = "6870628"
bot_url = "https://api.groupme.com/v3/bots/post"

app = Flask(__name__)

@app.route('/')
def hello():
	payload = { 'bot_id': configuration.bot_id,'text': "http://reddit.com/r/pics" }
	r = requests.post(configuration.bot_url, params=configuration.params, data=json.dumps(payload))
	return 'SPAM'

#@app.route('/ping')
#def ping():
#	payload = { 'bot_id': configuration.bot_id,'text': "http://reddit.com/r/pics" }
#	r = requests.post(configuration.bot_url, params=configuration.params, data=json.dumps(payload))
#	return 'OK'
