import os
import re
import random
from . import utility
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
#load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

first_answer_encoded = ''
first_answer = ''

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
    say("_as the sticky note says, 'GET OUT.'_")
    say("_look around for clues._")
    say("_you should probably look at the keypad by typing KEYPAD..._")


@app.message(re.compile("KEYPAD"))
def keypad_handle(message, say):
    say(f"_<@{message['user']}> looked at the keypad..._")
    say(f"_all it is doing is flashing the letters '{keypad_code()}'. for test reasons, the answer is {decode_keypad()}_")
    
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

@app.message(f"FIRST ANSWER {first_answer}")
def handle_first_answer(message, say):
	say(":yay:")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


def begin():
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()