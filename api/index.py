from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

questions = {
    1: "避免你與人界接觸過少，請你列出可以聽你說話的名單，給自己在喪失陽氣前留一條退路。",
    2: {
        "text": "你傷心的時候，前任怎麼安慰你？",
        "options": [
            "擁抱",
            "傳訊息說等他忙完後去找你",
            "他說一切都會變好",
            "會主動做些事說你小題大作",
            "他直接消失"
        ]
    },
    3: "你會做些甚麼避免自己憂傷沉淪？",
    4: "🗝如果的是"
}
answers = {}

def create_flex_message(question_number):
    question_data = questions.get(question_number)
    if isinstance(question_data, dict):
        return FlexSendMessage(
            alt_text=question_data["text"],
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": question_data["text"], "weight": "bold", "size": "xl"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {"type": "text", "text": option, "wrap": True, "color": "#666666", "size": "md", "flex": 0} for option in question_data["options"]
                            ]
                        }
                    ]
                }
            }
        )
    else:
        return None

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    current_question = len(answers)

    if current_question <= len(questions):
        answers[current_question] = user_message
        flex_message = create_flex_message(current_question + 1)

        if flex_message:
            line_bot_api.reply_message(
                event.reply_token,
                flex_message
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🗝如果的是")
            )
    else:
        pass

if __name__ == "__main__":
    app.run()
