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

class RegexResponder:
    def __init__(self, regex, regex_options, func):
        """ Construct a Responder that:
            1. matches a string against regex using regex_options
            2. passes matched groups to func
            3. returns func's result
        """
        self.regex = regex
        self.regex_options = regex_options
        self.func = func

    def matches(self, message):
        """ Check if message text matches self.regex """
        return bool(re.search(self.regex, message.text, self.regex_options))

    def respond_to(self, message):
        match_obj = re.search(self.regex, message.text, self.regex_options)
        if match_obj:
            return self.func(message, match_obj.groups())

def get_memes():
    memes = {}
    # get memes from imgflip
    memereq = requests.get(c.config['imgflip_get_memes']).json()
    if memereq['success']==True:
        memes = memereq['data']['memes']
    
    return memes


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
    logger.debug("meme wanted: {} -- {} -- {}".format(message.sender, message.text, groups))
    
    meme_id = groups[0].strip().lower().replace(' ', '_') if len(groups) > 0 else None
    line1 = groups[1] if len(groups) > 1 else None
    line2 = groups[2] if len(groups) > 2 else None
    
    logger.debug("doing meme: {} -- {} -- {}".format(meme_id, line1, line2))
    
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

            logger.debug("requesting meme with params: {}".format(str(params)))

            req = requests.post(c.config['imgflip_caption_image'], params=params).json()

            logger.debug("resulting request: {}".format(req))
            if req['success']:
                return [req['data']['url']]
    return []

def _y_u_no(message, groups):
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
        return [req['data']['url']]
    return []


__registered = []
def register(regex, re_opts, handler):
    __registered.append(RegexResponder(regex, re_opts, handler))

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
    for r in __registered:
        if r.matches(message):
            return r.respond_to(message)
