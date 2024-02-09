from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageCarouselTemplate,
MessageEvent, 
TextMessage,
TextSendMessage, 
ButtonsTemplate, 
TemplateSendMessage, 
MessageTemplateAction, 
CarouselTemplate, 
CarouselColumn,
ImageCarouselColumn, URITemplateAction)

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
def text_checker(event):
    user_msg=event.message.text
    if len(user_msg) >= 7 and user_msg[5] == "忍" and user_msg[6] == "受":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="不愧是怨靈，既然決定要怨恨希望你能堅定自己的決定，當然大多數選擇怨靈的都是一條路走到黑的。")
    ) 
        buttons_template = ButtonsTemplate(
            title="1",
            text="但為了防止您走火入魔，因此需要請您先進入善行靈堂，當你完成請按下世間美好",
            actions=[
                 URITemplateAction(label="網站連結", uri="https://www.google.com"),
                MessageTemplateAction(label="世間美好", text="世間美好"),
            ]
        )

        # 使用 TemplateSendMessage 包裝 ButtonsTemplate
        template_message = TemplateSendMessage(
            alt_text="選項",
            template=buttons_template
        )

        # 傳送 ButtonsTemplate 給使用者
        line_bot_api.push_message(
            event.source.user_id,
            template_message
        )
    elif len(user_msg) >= 7 and user_msg[4] == "生" and user_msg[5] == "命":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="不愧是愁靈，既然決定要怨恨希望你能堅定自己的決定，當然大多數選擇怨靈的都是一條路走到黑的。")
    )
        buttons_template = ButtonsTemplate(
            title="1",
            text="但為了防止您走火入魔，因此需要請您先進入善行靈堂，當你完成請按下世間美好",
            actions=[
                 URITemplateAction(label="網站連結", uri="https://www.google.com"),
                MessageTemplateAction(label="世間美好", text="世間美好"),
            ]
        )
         # 使用 TemplateSendMessage 包裝 ButtonsTemplate
        template_message = TemplateSendMessage(
            alt_text="選項",
            template=buttons_template
        )

        # 傳送 ButtonsTemplate 給使用者
        line_bot_api.push_message(
            event.source.user_id,
            template_message
        )
    elif len(user_msg) >= 7 and user_msg[0] == "我" and user_msg[5] == "曾":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="不愧是損靈，既然決定要怨恨希望你能堅定自己的決定，當然大多數選擇怨靈的都是一條路走到黑的。")
    )
        buttons_template = ButtonsTemplate(
            title="1",
            text="但為了防止您走火入魔，因此需要請您先進入善行靈堂，當你完成請按下世間美好",
            actions=[
                 URITemplateAction(label="網站連結", uri="https://www.google.com"),
                MessageTemplateAction(label="世間美好", text="世間美好"),
            ]
        )
         # 使用 TemplateSendMessage 包裝 ButtonsTemplate
        template_message = TemplateSendMessage(
            alt_text="選項",
            template=buttons_template
        )

        # 傳送 ButtonsTemplate 給使用者
        line_bot_api.push_message(
            event.source.user_id,
            template_message
        )

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

    text_checker(event)
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
        
    if user_message == "怨靈":
        textlist = []
        first_text = "怨靈不簡單啊，無論你是如何的，我們都會發揮完全的專業來超渡您。由於我們還不認識您，因此需要您提供一封休書，下面是休書的格式。*請您複製此格式並在框框中填入資料後回傳，過程中務必跟著心走。"
        sec_text = "我再也無法忍受我們之間的☐☐。愛情已死，而你是☐☐它的☐☐。我不再願意忍受你的☐☐。希望你過得☐☐，不再出現在我的生命中。"
        textlist.append(TextSendMessage(first_text))
        textlist.append(TextSendMessage(sec_text))
        line_bot_api.reply_message(
        event.reply_token,
        textlist
        )
        
    if user_message == "愁靈":
        textlist = []
        first_text = "愁靈好啊，無論你是如何的，我們都會發揮完全的專業來超渡您。由於我們還不認識您，因此需要您提供一封休書，下面是休書的格式。*請您複製此格式並在框框中填入資料後回傳，過程中務必跟著心走。"
        sec_text = "你曾是我生命中的☐☐，在曾經有你的日子裡我十分的☐☐。但事與願違，你曾在我眼裡是☐☐的存在，如今身分不同了，不會再像以前那樣☐☐。"
        textlist.append(TextSendMessage(first_text))
        textlist.append(TextSendMessage(sec_text))
        line_bot_api.reply_message(
        event.reply_token,
        textlist
        )
        
    if user_message == "損靈":
        textlist = []
        first_text = "損靈呀，無論你是如何的，我們都會發揮完全的專業來超渡您。由於我們還不認識您，因此需要您提供一封休書，下面是休書的格式。*請您複製此格式並在框框中填入資料後回傳，過程中務必跟著心走。"
        sec_text = "我曾以為你是我一生中☐☐的人，但因為你，如今我彷彿☐☐愛的能力。我以為我們是那麼的☐☐，但看來你並不那麼認為。你想☐☐結束的愛情，那我就成全你吧！"
        textlist.append(TextSendMessage(first_text))
        textlist.append(TextSendMessage(sec_text))
        line_bot_api.reply_message(
        event.reply_token,
        textlist
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
