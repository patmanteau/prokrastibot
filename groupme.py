# -*- coding: utf-8 -*-
""" Groupme API support
"""
import json
import requests
from config import config as c
# from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class ImageAttachment():
    """ Models a group.me Image Attachment
    """
    def __init__(self, url):
        """ Initialize with a URL.
        """
        self.url = url
        self.__type = 'image'

    def as_dict(self):
        """ Return the attachment as dict.
        """
        return {'type': self.__type, 'url': self.url}


class LocationAttachment():
    """ Models a group.me Location Attachment.
    """
    def __init__(self, lat, lng, name):
        """ Initialize with location and name.
        """
        self.lng = lng
        self.lat = lat
        self.name = name
        self.__type = 'location'

    def as_dict(self):
        """ Return the attachment as dict.
        """
        return {
            'type': self.__type,
            'lng': self.lng,
            'lat': self.lat,
            'name': self.name
        }


class BotMessage():
    """ A single response from a bot to group.me
    """
    def __init__(self, msg):
        self.bot_id = c['bot_id']
        self.text = msg.get('text', '')
        self.attachments = []

        location = msg.get('location', None)
        if location:
            self.add_attachment(
                LocationAttachment(
                    location['lat'],
                    location['lng'],
                    location['name']))

    def add_attachment(self, att):
        """ Add an attachment to this message.
        """
        self.attachments.append(att)

    def json(self):
        """ Return this message as JSON string.
        """
        payload = {'bot_id': self.bot_id, 'text': self.text}
        if len(self.attachments) > 0:
            atts_as_dict = [att.as_dict() for att in self.attachments]
            payload['attachments'] = atts_as_dict
        return json.dumps(payload)

    def empty(self):
        """ Check if this message is empty.
        """
        return (self.text == '') and (len(self.attachments) == 0)

    def __str__(self):
        return "{}: {}; attachments: {}".format(
            self.bot_id, self.text, self.attachments)


class BotCallback():
    """ A group.me callback message.
    """
    def __init__(self, jsn):
        """ Initialize a new BotCallback from a JSON string.
        """
        self.__raw = jsn
        self.sender = jsn.get('name', '')
        self.text = jsn.get('text', '')

        # self.attachments = jsn.get('attachments', [])
        # self.avatar_url = jsn.get('avatar_url', '')
        # self.created_at = datetime.fromtimestamp(
        #    int(jsn.get('created_at', '1302623328')))
        # self.group_id = jsn.get('group_id', '')
        # self._id = jsn.get('id', '')
        # self.sender_id = jsn.get('sender_id', '')
        # self.sender_type = jsn.get('sender_type', '')
        # self.source_guid = jsn.get('source_guid', '')
        # self.system = jsn.get('system', 'False')

    def __str__(self):
        return "{}: {}".format(self.sender, self.text)


def bot_send(message):
    """ Sends a bot message to groupme
    """
    if message is not None and not message.empty():
        params = {'token': c['access_token']}
        logger.debug("sending: %s", message)
        payload = message.json()

        logger.debug("payload: %s", payload)

        requests.post(c['bot_url'], params=params, data=payload)
    else:
        logger.debug("nothing to send")
