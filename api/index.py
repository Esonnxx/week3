from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, TemplateSendMessage, MessageTemplateAction, CarouselTemplate, CarouselColumn
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
def handle_follow(event):
    user_id = event.source.user_id

    # Customize your Buttons Template with an image here
    buttons_template = ButtonsTemplate(
        thumbnail_image_url="https://i.ibb.co/PYmQNYd/image.jpg",  # Replace with your image URL
        title="Welcome to the ChatBot!",
        text="Please choose an option:",
        actions=[
            MessageTemplateAction(label='同意', text='同意'),
            MessageTemplateAction(label='不同意', text='不同意'),
        ],
        image_aspect_ratio="rectangle"  # or "square"
    )

    template_message = TemplateSendMessage(
        alt_text="Welcome to the ChatBot!",
        template=buttons_template
    )

    # Send the Buttons Template message to the user
    line_bot_api.reply_message(
        event.reply_token,
        template_message
    )

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if user_message == "同意":
        # Customize your Carousel Template here
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://example.com/image1_thumbnail.jpg",  # Replace with your image URL
                    title="接任務",
                    text="接任務",
                    actions=[
                        MessageTemplateAction(label="接任務", text="接任務")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/image2_thumbnail.jpg",  # Replace with your image URL
                    title="幫助",
                    text="幫助",
                    actions=[
                        MessageTemplateAction(label="幫助", text="幫助")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/image3_thumbnail.jpg",  # Replace with your image URL
                    title="善行",
                    text="善行",
                    actions=[
                        MessageTemplateAction(label="善行", text="善行")
                    ]
                ),
            ]
        )

        carousel_message = TemplateSendMessage(
            alt_text="Image Carousel",
            template=carousel_template
        )

        line_bot_api.reply_message(
            event.reply_token,
            carousel_message
        )
    else:
        # Handle other messages or provide instructions
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please wait for the welcome message.")
        )

if __name__ == "__main__":
    app.run()
