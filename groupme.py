from config import config as c
import json
import requests

import logging
logger = logging.getLogger(__name__)

from datetime import datetime

class ImageAttachment():
    url = ''
    __type = ''

    def __init__(self, url):
        self.url = url
        self.__type = 'image'

    def as_dict(self):
        return {'type': self.__type, 'url': self.url}

class LocationAttachment():
    lng = ''
    lat = ''
    name = ''
    __type = ''

    def __init__(self, lat, lng, name):
        self.lng = lng
        self.lat = lat
        self.name = name
        self.__type = 'location'

    def as_dict(self):
        return {'type': self.__type, 'lng': self.lng, 'lat': self.lat, 'name': self.name}

class BotResponse():
    bot_id = ""
    text = ""
    attachments = []

    def __init__(self):
        self.bot_id = c['bot_id']

    def __init__(self, msg):
        self.bot_id = c['bot_id']
        self.text = msg

    def json(self):
        payload = {'bot_id': self.bot_id, 'text': self.text}
        if len(self.attachments) > 0:
            atts_as_dict = [att.as_dict() for att in self.attachments]
            payload['attachments'] = atts_as_dict
        return json.dumps(payload)

    def add_text(self, text):
        self.text = "".join(self.text, text)

    def add_text_ln(self, text):
        self.text = "\n".join(self.text, text)

    def empty(self):
        return (self.text == "") and (self.attachments.count() == 0)

    def __str__(self):
        return "{}: {}; attachments: {}".format(self.bot_id, self.text, self.attachments)

class Request():
    def __init__(self, jsn):
        self.__raw = jsn
        self.attachments = jsn.get('attachments', [])
        self.avatar_url = jsn.get('avatar_url', '')
        self.created_at = datetime.fromtimestamp(int(jsn.get('created_at', '1302623328')))
        self.group_id = jsn.get('group_id', '')
        self.id = jsn.get('id', '')
        self.sender = jsn.get('name', '')
        self.sender_id = jsn.get('sender_id', '')
        self.sender_type = jsn.get('sender_type', '')
        self.source_guid = jsn.get('source_guid', '')
        self.system = jsn.get('system', 'False')
        self.text = jsn.get('text', '')

    def __str__(self):
        return "{}: {}".format(self.sender, self.text)

def bot_send(bot_response):
    if bot_response != None and not bot_response.empty():
        params = {'token': c['access_token']}
        logger.debug("sending: {}".format(bot_response))
        payload = bot_response.json()

        logger.debug("payload: {}".format(payload))
    
        r = requests.post(c['bot_url'], params=params, data=payload)
    else:
        logger.debug("nothing to send")
