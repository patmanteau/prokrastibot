import os
import re
import requests
import json
import random
import config as c

class Responder:
	def __init__(self, regex, regex_options, func):
		""" Construct a Responder that:
		    1. matches a string against regex using regex_options
		    2. passes matched groups to func
		    3. returns func's result
		"""
		self.regex = regex
		self.regex_options = regex_options
		self.func = func

	def matches(self, string):
		""" Return True if string matches self.regex """
		return bool(re.search(self.regex, string, self.regex_options))

	def respond_to(self, name, text):
		match_obj = re.search(self.regex, text, self.regex_options)
		if match_obj:
			return self.func(name, text, match_obj.groups())

def get_memes():
	memes = {}
	# get memes from imgflip
	memereq = requests.get(c.config['imgflip_get_memes']).json()
	if memereq['success']==True:
		memes = memereq['data']['memes']
	
	return memes


def _prokrast(name, text, groups):
	data = requests.get("http://www.reddit.com/r/funny/rising.json").json()

	i = random.randint(0, len(data['data']['children'])-1)

	title = data['data']['children'][i]['data']['title']
	url = data['data']['children'][i]['data']['url']
	return (url, title)

known_memes = {
	'overly_manly_man': '247756',
	'peter_griffin_news': '356615',
	'dj_pauly_d': '2005809',
	'captain_hindsight': '101708',
	'grumpy_cat': '405658',
	'ermahgerd_berks': '101462',
	'scumbag_steve': '61522',
	'batman_slapping_robin': '438680',
	'one_does_not_simply': '61579',
	'jack_sparrow_being_chased': '460541',
	'dont_you_squidward': '101511',
	'first_day_on_the_internet_kid': '71851',
	'creepy_condescending_wonka': '61582',
	'skeptical_baby': '101711',
	'confession_kid': '2141397',
	'y_u_no': '61527',
	'angry_baby': '146381',
	'the_rock_driving': '21735',
	'overly_attached_girlfriend': '100952',
	'spiderman_peter_parker': '107773',
	'conspiracy_keanu': '61583',
	'insanity_wolf': '61518',
	'third_world_success_kid': '101287',
	'kevin_hart_the_hell': '265789',
	'imagination_spongebob': '163573',
	'confused_gandalf': '673439',
	'yo_dawg_heard_you': '101716',
	'baby_godfather': '101704',
	'picard_wtf': '245898',
	'put_it_somewhere_else_patrick': '61581',
	'yao_ming': '109015',
	'pepperidge_farm_remembers': '1232104',
	'third_world_skeptical_kid': '101288',
	'unpopular_opinion_puffin': '7761261',
	'simba_shadowy_place': '371382',
	'weird_stuff_i_do_potoo': '10747721',
	'see_nobody_cares': '6531067',
	'too_damn_high': '61580',
	'sudden_clarity_clarence': '100948',
	'ted': '131092',
	'ill_just_wait_here': '109765',
	'buddy_christ': '17699',
	'disaster_girl': '97984',
	'back_in_my_day': '718432',
	'x_all_the_y': '61533',
	'inception': '156892',
	'lion_king': '206153',
	'x_x_everywhere': '347390',
	'sparta_leonidas': '195389',
	'keep_calm_and_carry_on_red': '1202623',
	'joseph_ducreux': '61535',
	'say_that_again_i_dare_you': '124212',
	'ryan_gosling': '389834',
	'impossibru_guy_original': '307405',
	'boardroom_meeting_suggestion': '1035805',
	'i_know_fuck_me_right': '2182291',
	'and_everybody_loses_their_minds': '1790995',
	'finding_neverland': '6235864',
	'gollum': '681831',
	'ancient_aliens': '101470',
	'maury_lie_detector': '444501',
	'skinhead_john_travolta': '963245',
	'unhelpful_high_school_teacher': '100957',
	'matrix_morpheus': '100947',
	'that_would_be_great': '563423',
	'aaaaand_its_gone': '766986',
	'i_should_buy_a_boat_cat': '1367068',
	'good_guy_greg': '61521',
	'am_i_the_only_one_around_here': '259680',
	'captain_picard_facepalm': '1509839',
	'futurama_fry': '61520',
	'dr_evil_laser': '221020',
	'drunk_baby': '100944',
	'ron_burgundy': '1232147',
	'success_kid': '61544',
	'evil_toddler': '235589',
	'bad_luck_brian': '61585',
	'confession_bear': '100955',
	'so_i_got_that_goin_for_me_which_is_nice': '8774527',
	'pissed_off_obama': '306319',
	'first_world_problems': '61539',
	'neil_degrasse_tyson': '109017',
	'liam_neeson_taken': '228024',
	'slowpoke': '61530',
	'kill_yourself_guy': '172314',
	'so_i_guess_you_can_say_things_are_getting_pretty_serious': '816349',
	'brace_yourselves_x_is_coming': '61546', 
	'aint_nobody_got_time_for_that': '442575',
	'grandma_finds_the_internet': '61556',
	'i_too_like_to_live_dangerously': '646581',
	'spiderman_computer_desk': '1366993',
	'socially_awesome_awkward_penguin': '61584',
	'success_kid_original': '341570',
	'super_cool_ski_instructor': '100951',
	'ten_guy': '101440',
	'the_most_interesting_man_in_the_world': '61532',
	'actual_advice_mallard': '1356640',
	'philosoraptor': '61516',
	'laughing_men_in_suits': '922147',
	'doge': '8072285'
}

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

def _memelist(name, text, groups):
	return "https://dl.dropboxusercontent.com/u/2530719/memelist.html"
	
def _meme(name, text, groups):
	meme_id = groups[0] if len(groups) > 0 else None
	line1 = groups[1] if len(groups) > 1 else None
	line2 = groups[2] if len(groups) > 2 else None

	print(meme_id)
	print(line1) 
	print(line2)

	if meme_id:
		#memes = get_memes()
		if meme_id in known_memes:
			params = {
				'template_id': known_memes[meme_id],
				'username': c.config['imgflip_username'],
				'password': c.config['imgflip_password']
			}
			if line1:
				params['text0'] = line1
			if line2:
				params['text1'] = line2

			req = requests.post(c.config['imgflip_caption_image'], params=params).json()
			if req['success']:
				return req['data']['url']
	return None

def _help(name, text, groups):
	return [
		"!memelist: Bekannte Memes",
		"!meme <id>|text0|text1: Erzeugt das Meme <id> mit den angegebenen Texten. Die | sind mandatorisch, auch wenn nur text0 übergeben werden soll."
	]

class Dispatcher:
	def __init__(self):
		self.registered = []

		self.register(Responder('^!help',
								re.I,
								_help))
		self.register(Responder('^!memelist',
								re.I,
								_memelist))
		self.register(Responder('^!meme (.+)\|(.+)\|(.*)',
								re.I,
								_meme))
		self.register(Responder('prokrast',
								re.I,
								_prokrast))
		self.register(Responder('kann[\w ]*nicht', 
								re.I, 
								lambda name, text, groups:
									"kann-nicht wohnt in der will-nicht-straße, {}".format(name)))
	


	def register(self, responder):
		self.registered.append(responder)

			
	def answer(self, name, text):
		for r in self.registered:
			if r.matches(text):
				return r.respond_to(name, text)
	