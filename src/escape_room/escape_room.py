import os
import re
import random
import time
from dotenv import load_dotenv
from . import utility
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv(dotenv_path='./.env')

app = App(token=os.getenv('SLACK_BOT_TOKEN'))

first_answer_encoded = ''
first_answer = ''
has_key = False

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
	global first_answer_encoded
	first_answer_encoded = ''
	ack()
	respond(f"_<@{body['user']['id']}>_ started!")
	say("_you are in a room, with a large vault door in front of you. there is a small sticky note on the door. it reads: 'GET OUT. -anonymous'_")
	say("_to the right, there is a keypad on something that looks like a vault..._")
	say("_behind you there is a box with a keyhole._")
	say("_as the sticky note says, GET OUT._")
	say("_look around for clues, and have fun!_")
	say("_you should probably look at the keypad by typing 'KEYPAD'..._")
	say("_you can also look at the box with 'BOX'._")


@app.message(re.compile("KEYPAD"))
def keypad_handle(message, say):
	say(f"_<@{message['user']}> looked at the keypad..._")
	say(f"_all it is doing is flashing the letters '{keypad_code()}'._")
	say("_if you need a hint, type 'FIRST CLUE'._")
	say("*when you have an answer, or a guess, type 'FIRST ANSWER [answer]'. have fun!*")
    
def keypad_code():
	global first_answer_encoded
	if first_answer_encoded == '':
		a = []
		alphabet = 'abcdefghi'
		for _ in range(4):
			a.append(random.choice(alphabet))
		first_answer_encoded = ''.join(a)
		return first_answer_encoded
	else:
		return first_answer_encoded

def decode_keypad():
	global first_answer, first_answer_encoded
	answer = []
	for i in first_answer_encoded:
			answer.append(str(utility.map_alpha_to_numbers(i)))

	first_answer = ''.join(answer)
	return first_answer

@app.message('FIRST CLUE')
def handle_first_clue(say):
	say(
		f"""
		_the keypad is laid out like this:_

		1 2 3
		4 5 6
		7 8 9
		   0  
		
		_what relation does '{first_answer_encoded}' have to those numbers?_
		"""
	)
	say("_that was your first clue._")

@app.message(f"FIRST ANSWER {first_answer}")
def handle_first_answer(message, say):
	global first_puzzle_complete
	first_puzzle_complete = True
	say(":yay: you figured it out!")
	say("_Inside the vault, you find a large piece of paper, with the following..._") 
	time.sleep(0.25)
	say("_uh actually,_") 
	say("_why don't I just show you the paper?_")
	blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "_in cyber space, the paper resides here: https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png. _"
			}
		},
		{
			"type": "image",
			"image_url": "https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png",
			"alt_text": "'VWLU ZLZHTL' zlltz av dvyr"
		}
	]
	say(blocks=blocks, text="_in cyberspace, the paper resides here: https://hc-cdn.hel1.your-objectstorage.com/s/v3/756ed2af422576e762736dd33e4f0c46ac450c94_vwlu_zlzhtl.png _")
	say("_(if you hover over it, it should tell you the text in the image...)_")

@app.message("OPEN SESAME")
def handle_second_puzzle_answer(say):
	global first_puzzle_complete
	say("_you say the words into the empty room._")
	say("_a panel in the wall that you didn't know existed pops out and reveals a secceret compartement._")
	say("_inside the compartment there is a key._")
	say("*type KEY to go over and pick up the key.*")

@app.message(re.compile("KEY"))
def handle_key_message(say):
	global has_key
	has_key = True
	say("_you walk over and pick up the key._")
	say("_what do you think it could open?_")
	say("_psst_")
	say("_if you need a clue, type 'SECOND CLUE'.")

@app.message("SECOND CLUE")
def handle_second_clue(say):
	global first_puzzle_complete
	if first_puzzle_complete:
		say("clue")
	else:
		say("_You found this by accident! do this later_")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


def begin():
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()