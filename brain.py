# -*- coding: utf-8 -*- 

import requests
import os
import json
import re
import random
import config as c
import groupme
import logging
import functools
logger = logging.getLogger(__name__)

__registered_handlers = {}


def regex_handler(regex, regex_opts):
    def regex_handler_decorator(func):
        @functools.wraps(func)
        def wrapped(message):
            match_obj = re.search(regex, message.text, regex_opts)
            if match_obj:
                a = func(message, match_obj.groups())
                if a:
                    return a
            return None

        __registered_handlers[regex] = wrapped
        return wrapped

    return regex_handler_decorator


@regex_handler('prokrast', re.I)
def _prokrast(message, groups):
    logger.debug("getting link")

    headers = {'User-Agent': 'prokrastibot/1.0'}
    subreddit = "http://www.reddit.com/r/funny/rising.json" if random.randint(1, 10) > 1 else "http://www.reddit.com/r/Motivational/rising.json"
    data = requests.get(subreddit, headers=headers).json()

    posts = data['data']['children']
    if len(posts) > 1:
        i = random.randint(0, len(posts)-1)

        title = posts[i]['data']['title']
        url = posts[i]['data']['url']

        logger.debug("title: {} url: {}".format(title, url))

        return [{'text': url}, {'text': title}]
    else:
        return []


@regex_handler('^wo ist (.+)', re.I)
def _find_position(message, groups):
    logger.debug('_find_position: {}, {}'.format(message, groups))

    address = groups[0].strip().lower().replace(' ', '+') if len(groups) > 0 else None
    params = {
        'address': address,
        'sensor': 'false'
    }

    req = requests.post(c.config['gmaps_url'], params=params).json()

    if req['status'] == 'OK':
        formatted_address = req['results'][0]['formatted_address']
        location = req['results'][0]['geometry']['location']
        lat, lng = location['lat'], location['lng']
        return [ { 
                'text': '',
                'location': { 'lat': lat, 'lng': lng, 'name': formatted_address}
        } ]
    else:
        return []



@regex_handler('^!meme (.+)\|(.+)\|(.*)', re.I)
def _meme(message, groups):
    logger.debug('_meme: {}, {}'.format(message, groups))

    meme_id = groups[0].strip().lower().replace(' ', '_') if len(groups) > 0 else None
    if meme_id in c.known_memes:
        params = {
            'template_id': c.known_memes[meme_id],
            'username': c.config['imgflip_username'],
            'password': c.config['imgflip_password'],
            'text0': groups[1] if len(groups)>1 else '',
            'text1': groups[2] if len(groups)>2 else '',
        }

        logger.debug("_meme: requesting imgflip meme (params: {})".format(str(params)))
        req = requests.post(c.config['imgflip_caption_image'], params=params).json()
        if req['success']:
            return [ {'text': req['data']['url']} ]
    return []


@regex_handler('^(y u no) (.+)', re.I)
def _y_u_no(message, groups):
    meme_id = c.known_memes['y_u_no']
    params = {
        'template_id': meme_id,
        'username': c.config['imgflip_username'],
        'password': c.config['imgflip_password'],
        'text0': groups[0] if len(groups)>0 else '',
        'text1': groups[1] if len(groups)>1 else '',
    }

    req = requests.post(c.config['imgflip_caption_image'], params=params).json()

    if req['success']:
        return [ {'text': req['data']['url']} ]
    else:
        return []


@regex_handler('^!help', re.I)
def _bang_help(message, groups):
    return [
        { 'text': '!memelist: Bekannte Memes' },
        { 'text': '!meme <id>|text0|text1: Erzeugt das Meme <id> mit den angegebenen Texten. Die | sind mandatorisch, auch wenn nur text0 übergeben werden soll.'}
    ]


@regex_handler('^!memelist', re.I)
def _bang_memelist(message, groups):
    return [
        { 'text': 'https://dl.dropboxusercontent.com/u/2530719/memelist.html' }
    ]


@regex_handler('^awesome', re.I)
def _awesome(message, groups):
    return [
        { 'text': 'http://ownyourawesome.files.wordpress.com/2012/09/awesome-meter.jpg' }
    ]


@regex_handler('kann[\w ]*nicht', re.I)
def _kann_nicht(message, groups):
    return [
        { 'text': 'kann-nicht wohnt in der will-nicht-straße, {}'.format(message.sender) }
    ]


def answer(message):
    for regex, handler in __registered_handlers.items():
        a = handler(message)
        if a:
            return a
    return []


