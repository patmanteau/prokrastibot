# -*- coding: utf-8 -*-
""" Contains chatbot functionality.
"""

import requests
import re
import random
import config as c
import logging
import functools
logger = logging.getLogger(__name__)

__registered_handlers = {}


def regex_handler(regex, regex_opts):
    """ Internal regex decorator maker.
    """
    def regex_handler_decorator(func):
        """ Internal decorator for regex handlers
        """
        @functools.wraps(func)
        def wrapped(message):
            """ Apply a regex against the message's text.
                If it matches, call the decorated func passing
                the original message and the regex's matched groups.
                Return None if no match.
            """
            match_obj = re.search(regex, message.text, regex_opts)
            if match_obj:
                result = func(message, match_obj.groups())
                if result:
                    return result
            return None

        __registered_handlers[regex] = wrapped
        return wrapped

    return regex_handler_decorator


@regex_handler(r'prokrast', re.I)
def _prokrast(message, groups):
    """ Return a random reddit image link.
    """
    logger.debug("getting link")

    headers = {'User-Agent': 'prokrastibot/1.0'}
    subreddit = {
        True: 'http://www.reddit.com/r/funny/rising.json',
        False: 'http://www.reddit.com/r/Motivational/rising.json'
    }[random.randint(1, 10) > 1]

    data = requests.get(subreddit, headers=headers).json()
    posts = data['data']['children']
    if len(posts) > 1:
        i = random.randint(0, len(posts)-1)
        title = posts[i]['data']['title']
        url = posts[i]['data']['url']
        logger.debug("title: %s url: %s", title, url)

        return [{'text': url}, {'text': title}]
    else:
        return []


@regex_handler(r'^wo ist (.+)', re.I)
def _find_position(message, groups):
    """Lookup an address at Google Maps and return the result
        as dict.
    """
    logger.debug('_find_position: %s, %s', message, groups)

    if len(groups) > 0:
        address = groups[0].strip().lower().replace(' ', '+')
        params = {
            'address': address,
            'sensor': 'false'
        }

        req = requests.post(c.config['gmaps_url'], params=params).json()

        if req['status'] == 'OK':
            formatted_address = req['results'][0]['formatted_address']
            location = req['results'][0]['geometry']['location']
            lat, lng = location['lat'], location['lng']
            return [{
                'text': '',
                'location': {
                    'lat': lat,
                    'lng': lng,
                    'name': formatted_address
                }}]
    return []


@regex_handler(r'^!meme (.+)\|(.+)\|(.*)', re.I)
def _meme(message, groups):
    """Use imgflip to create a meme and return its URL.
    """
    logger.debug('_meme: %s, %s', message, groups)

    if len(groups) > 0:
        meme_id = groups[0].strip().lower().replace(' ', '_')
        if meme_id in c.known_memes:
            params = {
                'template_id': c.known_memes[meme_id],
                'username': c.config['imgflip_username'],
                'password': c.config['imgflip_password'],
                'text0': groups[1] if len(groups) > 1 else '',
                'text1': groups[2] if len(groups) > 2 else '',
            }

            logger.debug("_meme: imgflip meme (%s)", str(params))
            req = requests.post(
                c.config['imgflip_caption_image'], params=params).json()
            if req['success']:
                return [{'text': req['data']['url']}]
    return []


@regex_handler(r'^(y u no) (.+)', re.I)
def _y_u_no(message, groups):
    """Use imgflip to create a Y U NO meme and return its URL.
    """
    meme_id = c.known_memes['y_u_no']
    params = {
        'template_id': meme_id,
        'username': c.config['imgflip_username'],
        'password': c.config['imgflip_password'],
        'text0': groups[0] if len(groups) > 0 else '',
        'text1': groups[1] if len(groups) > 1 else '',
    }

    req = requests.post(
        c.config['imgflip_caption_image'], params=params).json()

    if req['success']:
        return [{'text': req['data']['url']}]
    else:
        return []


@regex_handler(r'^!help', re.I)
def _bang_help(message, groups):
    """Return a help text for all bang commands.
    """
    return [
        {'text': '!memelist: Bekannte Memes'},
        {'text': '!meme <id>|text0|text1: Erzeugt das Meme <id> mit den'
                 'angegebenen Texten. Die | sind mandatorisch, auch wenn'
                 ' nur text0 übergeben werden soll.'}
    ]


@regex_handler(r'^!memelist', re.I)
def _bang_memelist(message, groups):
    """Return the URL of a list of supported memes.
    """
    return [
        {'text': 'https://dl.dropboxusercontent.com/'
                 'u/2530719/memelist.html'}
    ]


@regex_handler(r'^awesome', re.I)
def _awesome(message, groups):
    """Tell everyone they're awesome!
    """
    return [
        {'text': 'http://ownyourawesome.files.wordpress.com/'
                 '2012/09/awesome-meter.jpg'}
    ]


@regex_handler(r'kann[\w ]*nicht', re.I)
def _kann_nicht(message, groups):
    """Return a certain quip referring to a specific user.
    """
    return [
        {'text': 'kann-nicht wohnt in der will-nicht-straße,'
                 ' {}'.format(message.sender)}
    ]


def answer(message):
    """ Lookup and execute the first matching handler for a message.
        Return the result.
    """
    for regex, handler in __registered_handlers.items():
        result = handler(message)
        if result:
            return result
    return []
