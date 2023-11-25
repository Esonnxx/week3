from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from linebot.models.events import FollowEvent, MessageEvent, TextMessage
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 設定問題與答案的字典
questions = {
    1: "你今年幾歲",
    2: "你的性別",
    3: "你的名字",
    4: "謝謝！問題結束。"
}
answers = {}
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

    current_question = len(answers) 

    if current_question <= len(questions):
        answers[current_question] = user_message
        next_question = questions.get(current_question + 1)

        if next_question:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=next_question)
            )
        else:
            # 所有問題都已回答，可以在這裡進行其他操作
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="謝謝！問題結束。")
            )
    else:
        # 多餘的回答或其他處理方式
        pass

if __name__ == "__main__":
    app.run()