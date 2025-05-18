import os
import re
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))



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
def handle_begin(ack, say, body):
    ack()
    say("hello!")

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

def begin():
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()