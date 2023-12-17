from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from linebot.models.events import FollowEvent, MessageEvent, TextMessage
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.add(FollowEvent)
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if user_message == "我同意":
        # Customize your options after user agrees
        quick_reply_buttons = [
            QuickReplyButton(action=MessageAction(label="Option 1", text="Option 1")),
            QuickReplyButton(action=MessageAction(label="Option 2", text="Option 2")),
            # Add more buttons as needed
        ]

        quick_reply_message = TextSendMessage(
            text="Choose an option:",
            quick_reply=QuickReply(items=quick_reply_buttons)
        )

        line_bot_api.reply_message(
            event.reply_token,
            quick_reply_message
        )
    else:
        # Handle other messages or provide instructions
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please type '我同意' to proceed.")
        )

if __name__ == "__main__":
    app.run()