# -*- coding: utf-8 -*- 

import requests
import os
import json
import re
import random
import config as c
import groupme
import logging
logger = logging.getLogger(__name__)


def _prokrast(message, groups):
    logger.debug("getting link")

    headers = {'User-Agent': 'prokrastibot/1.0'}
    subreddit = "http://www.reddit.com/r/funny/rising.json" if random.randint(1, 10) > 1 else "http://www.reddit.com/r/Motivational/rising.json"
    data = requests.get(subreddit, headers=headers).json()

    i = random.randint(0, len(data['data']['children'])-1)

    title = data['data']['children'][i]['data']['title']
    url = data['data']['children'][i]['data']['url']

    logger.debug("title: {} url: {}".format(title, url))

    return [url, title]


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def _meme(message, groups):
    """ 
    """
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
            return [req['data']['url']]
    return []


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
        return [req['data']['url']]
    else:
        return []


__registered = {}
def register(regex, regex_opts, func):
    __registered[regex] = {
        'regex_opts': regex_opts,
        'func': func,
    }


register('^!meme (.+)\|(.+)\|(.*)', re.I, _meme)
register('^(y u no) (.+)', re.I, _y_u_no)
register('prokrast', re.I, _prokrast)
register('^!help', re.I,
    lambda message, groups:
        [
            "!memelist: Bekannte Memes",
            "!meme <id>|text0|text1: Erzeugt das Meme <id> mit den angegebenen Texten. Die | sind mandatorisch, auch wenn nur text0 übergeben werden soll."
        ]
)
register('^!memelist', re.I, 
    lambda message, groups:
        ["https://dl.dropboxusercontent.com/u/2530719/memelist.html"]
)
register(
    '^awesome', re.I,
    lambda message, groups:
        ["http://ownyourawesome.files.wordpress.com/2012/09/awesome-meter.jpg"]
)
register(
    'kann[\w ]*nicht', re.I, 
    lambda message, groups:
        ["kann-nicht wohnt in der will-nicht-straße, {}".format(message.sender)]
)
    

def answer(message):
    for regex, handler in __registered.items():
        match_obj = re.search(regex, message.text, handler['regex_opts'])
        if match_obj:
            a = handler['func'](message, match_obj.groups())
            if a:
                return a
    return []
