from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import ImageCarouselTemplate,MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, TemplateSendMessage, MessageTemplateAction, CarouselTemplate, CarouselColumn,ImageCarouselColumn
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

    # Define Image Carousel Template
    image_carousel_template = ImageCarouselTemplate(
    columns=[
        ImageCarouselColumn(
            image_url="https://i.ibb.co/PYmQNYd/image.jpg",  # Replace with your image URL
            action=MessageTemplateAction(
                label='Play',
                text='Play'
            )
        ),
    ]
)
# Create Template Message with Image Carousel Template
    template_message = TemplateSendMessage(
        alt_text="Welcome to the ChatBot!",
        template=image_carousel_template
    )

# Send the Image Carousel Template message to the user
    line_bot_api.reply_message(
    event.reply_token,
    template_message
)
   

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if user_message == "Play":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="每個人在經歷被分手都會有不同的反應，因此請您思考一下自己的個性，選擇一個符合您自己的靈種，他將會映射出您自己。")
        )
        image_carousel_template = ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url="https://i.ibb.co/PYmQNYd/image.jpg",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='怨靈',
                    text='怨靈'
                )
            ),
            ImageCarouselColumn(
                image_url="https://i.ibb.co/PYmQNYd/image.jpg",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='愁靈',
                    text='愁靈'
                )
            ),
            ImageCarouselColumn(
                image_url="https://i.ibb.co/PYmQNYd/image.jpg",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='損靈',
                    text='損靈'
                )
            ),
            
        ]
    )

    # 建立 Template Message 包含 Image Carousel Template
    template_message = TemplateSendMessage(
        alt_text="Welcome to the ChatBot!",
        template=image_carousel_template
    )

    # 回傳 Image Carousel Template 給使用者
    line_bot_api.push_message(
        event.source.user_id,
        template_message
    )


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
