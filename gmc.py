import configuration
import requests
import json

def main():
	payload = {
		'bot_id': configuration.bot_id,
		'text': "http://reddit.com/r/pics"
	}
	r = requests.post(configuration.bot_url, params=configuration.params, data=json.dumps(payload))
	print(r.status_code)
	# print(r.json())


if __name__=="__main__":
	main()