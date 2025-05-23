import os
import re
import random
from dotenv import load_dotenv
from . import utility
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv(dotenv_path='./.env')

app = App(token=os.getenv('SLACK_BOT_TOKEN'), signing_secret=os.getenv('SLACK_SIGNING_SECRET'))

first_answer_encoded = ''
first_answer = ''
first_puzzle_complete = False
has_key = False

second_puzzle_finished = False

@app.message(re.compile("START"))
def start_message(message, say):
    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"hello, _<@{message['user']}>_! would you like to start?"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "begin",
						"emoji": True
					},
					"value": "begin",
					"action_id": "begin"
				}
			]
		}
	]
    
    say(blocks=blocks, text=f"hello, _<@{message['user']}>_! would you like to begin?")


@app.action("begin")
def handle_begin(ack, say, body, respond):
	ack()
	utility.initialize_new_session(body['container']['channel_id'])
	respond(f"_<@{body['user']['id']}>_ started!")
	say("_you are in a room, with a large door with a large keypad on it in front of you. there is a small sticky note on the door. it reads: 'GET OUT. -anonymous'_")
	say("_to the right, there is a 9-digit keypad on something that looks like a container of some kind..._")
	say("_behind you there is a box with a keyhole._")
	say("_as the sticky note says, GET OUT._")
	say("_look around for clues, and have fun!_")
	say("_you should probably look at the keypad by typing 'KEYPAD'..._")
	say("_you can also look at the box with 'BOX'._")


@app.message(re.compile("KEYPAD"))
def keypad_handle(message, say):
	say(f"_<@{message['user']}> looked at the keypad..._")
	say(f"_all it is doing is flashing the letters '{keypad_code(message['channel'])}'._")
	say("_if you need a hint, type 'FIRST CLUE'._")
	say("*when you have the answer, or a guess, type 'FIRST ANSWER [answer]'. have fun!*")

def keypad_code(channel):
	global first_answer_encoded
	
	first_answer_encoded = utility.get_value('first_answer_encoded',channel)
	print("a", channel)
	if first_answer_encoded == '':
		a = []
		alphabet = 'abcdefghi'
		for _ in range(4):
			a.append(random.choice(alphabet))
		first_answer_encoded = ''.join(a)
		print('b',channel)
		utility.update_value('first_answer_encoded', first_answer_encoded, channel)
		utility.update_value('first_answer', decode_keypad(channel), channel)
		print(utility.get_value('first_answer', channel))
		return first_answer_encoded
	else:
		return first_answer_encoded

def decode_keypad(channel):
	print('c', channel)
	global first_answer_encoded
	answer = []
	string = utility.get_value('first_answer_encoded', channel)
	for i in string:
			answer.append(str(utility.map_alpha_to_numbers(i)))

	a = ''.join(answer)
	utility.update_value('first_answer', a, channel)
	return a

@app.message('FIRST CLUE')
def handle_first_clue(message, say):
	say(
		f"""
		_the keypad is laid out like this:_

		1 2 3
		4 5 6
		7 8 9
		   0  
		
		_what relation does '{utility.get_value('first_answer_encoded', message['channel'])}' have to those numbers?_
		"""
	)
	say("_that was your first clue._")

# @app.message(f"FIRST ANSWER {first_answer}")
# def handle_first_answer(message, say):
# 	global first_puzzle_complete
# 	first_puzzle_complete = True
# 	say(":yay: you figured it out!")
# 	say("_Inside the vault, you find a large piece of paper, with the following..._") 
# 	say("_uh actually,_") 
# 	say("_why don't I just show you the paper?_")
# 	blocks = [
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "_the paper looks like this:_"
# 			}
# 		},
# 		{
# 			"type": "image",
# 			"image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png",
# 			"alt_text": "'VWLU ZLZHTL' zlltz av dvyr"
# 		}
# 	]
# 	say(blocks=blocks, text="_in cyberspace, the paper resides here: https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png _")
# 	say("_(if you hover over it, it should tell you the text in the image...)_")

@app.message("OPEN SESAME")
def handle_second_puzzle_answer(message, say):
	say("_you say the words into the empty room._")
	say("_a panel in the wall that you didn't know existed pops out and reveals a secceret compartement._")
	say("_inside the compartment there is a key._")
	say("*type KEY to go over and pick up the key.*")
	utility.update_value('second_puzzle_finished', True, message['channel'])

@app.message(re.compile("^KEY$"))
def handle_key_message(message, say):
	# global has_key
	# has_key = True
	if utility.get_value('second_puzzle_finished', message['channel']):
		say("_you walk over and pick up the key._")
		say("_what do you think it could open?_")
		say("_if you need a clue, type 'SECOND CLUE'._")
		utility.update_value('has_key', True, message['channel'])
	else:
		say("_what key?_")

@app.message("SECOND CLUE")
def handle_second_clue(message, say):
	global first_puzzle_complete
	if utility.get_value('has_key', message['channel']):
		say("_try typing 'BOX'. that will lead you in the right direction..._")
	else:
		say("_You found this by accident! do this later_")

@app.message("BOX")
def handle_box(message, say):
	global has_key, second_puzzle_finished
	if utility.get_value('has_key', message['channel']):
		say("_you take the key and insert it into the box..._")
		say("_the box opens and reveals a hastily drawn sticky note..._")
		blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "_this is what it looks like:_"
			}
		},
		{
			"type": "image",
			"image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/1c8c5e9bdbf50226168447978c41c0d9b4e8f77b_puzzle.png",
			"alt_text": "a keypad with lines... this one you kinda need to see lol"
		}
		]
		say(blocks=blocks, text="_this is what it looks like:_")
		say("hmm... If I didn't know any better, this looks like a clue!")
		say("if you solve it, type 'FINAL PUZZLE [code]'")
	else:
		say("_you look at the box..._")
		say("_the box looks bare except for a single keyhole..._")

# @app.message('FINAL PUZZLE 07*846#5')
# def handle_final_answer(say):
# 	say(":yay: you got out :yay:")

@app.action('ceaser_clue')
def handle_ceaser_clue(ack, say, body, respond):
	ack()
	say("_your hint: the text is a ceaser cipher..._")

@app.event('message')
def handle_message_events(body, logger, say):
	#print(body)
	try:
		a = utility.get_value('first_answer', body['event']['channel'])
	except KeyError:
		a = ''
	
	# print(a)
	try:
		if body['event']['text'] == 'FINAL PUZZLE 07*846#5':
			say(":yay: you got out! :yay:")
			say("thanks for playing!")
		elif body['event']['text'] == f'FIRST ANSWER {a}':
			utility.update_value('first_puzzle_complete', True, body['event']['channel'])
			say("_Inside the vault, you find a large piece of paper, with the following..._") 
			say("_uh actually,_") 
			say("_why don't I just show you the paper?_")
			blocks = [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "_the paper looks like this:_"
					}
				},
				{
					"type": "image",
					"image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png",
					"alt_text": "'VWLU ZLZHTL' zlltz av dvyr"
				},
				{
					"type": "actions",
					"elements": [
						{
							"type": "button",
							"text": {
								"type": "plain_text",
								"text": "clue",
								"emoji": True
							},
							"value": "clue",
							"action_id": "ceaser_clue"
						}
					]
				}
			]
			say(blocks=blocks, text="_in cyberspace, the paper resides here: https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png _")
			say("_(if you hover over it, it should tell you the text in the image...)_")

	except Exception:
		logger.info(body)


def begin(http=False, port=3000):
	if http:
		app.start(port=int(port))
	else:
		SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()