
from flask import Flask, request
from pymessanger.bot import Bot

# constant config values
ACCESS_TOKEN = "ACCESS_TOKEN"
VERIFY_TOKEN = "VERIFY_TOKEN"
bot = Bot(ACCESS_TOKEN)

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def receive_message():
    if (request.method == "GET"):
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        # POST request; get message user sent to bot
        output = request.get_json()
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                if message.get("message"):
                    # get messanger id of user
                    recipient_id = message["sender"]["id"]

                    # may have text
                    if message["message"].get("text"):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)

                    # may have attachments
                    if message["message"].get("attachments"):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message processed"

def get_message():
    # logic used to generate response
    return "Hello world!"


def verify_fb_token(token_sent):
    # confirm token received and sent match
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification code"

def send_message(recipient_id, response):
    # sends user message
    bot.send_text_message(recipient_id, response)
    return "success"




if (__name__ == '__main__'):
    app.run()

