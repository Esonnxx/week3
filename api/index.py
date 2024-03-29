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
ConfirmTemplate,
FlexSendMessage,
ImageCarouselColumn, 
URITemplateAction,
QuickReply, 
QuickReplyButton,
MessageAction)
from linebot.models.events import FollowEvent, MessageEvent, TextMessage
from api.chatgpt import ChatGPT
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = False

 
chatgpt = ChatGPT()


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

def create_buttons_template(text, action_label, action_text):
    buttons_template = ButtonsTemplate(
        title=" ",
        text=text,
        actions=[
            MessageTemplateAction(label=action_label, text=action_text),
        ]
    )

    template_message = TemplateSendMessage(
        alt_text="選項",
        template=buttons_template
    )

    return template_message

def create_buttons_template_with_url(text, label_url,url, action_label, action_text):
    buttons_template = ButtonsTemplate(
        title=" ",
        text=text,
        actions=[
            URITemplateAction(label=label_url, uri=url),
            MessageTemplateAction(label=action_label, text=action_text),
        ]
    )

    template_message = TemplateSendMessage(
        alt_text="選項",
        template=buttons_template
    )

    return template_message



def text_checker(event):
    working_status =False
    user_msg=event.message.text
    if len(user_msg) >= 7 and user_msg[5] == "忍" and user_msg[6] == "受":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="不愧是怨靈，既然決定要怨恨希望你能堅定自己的決定，當然大多數選擇怨靈的都是一條路走到黑的。")
    ) 
        buttons_template = ButtonsTemplate(
            title=" ",
            text="但為了防止您走火入魔，因此需要請您先進入善行靈堂，當你完成請按下世間美好",
            actions=[
                 URITemplateAction(label="善行靈堂", uri="http://benevolence2.0.s3-website-ap-northeast-1.amazonaws.com"),
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
    elif len(user_msg) >= 7 and user_msg[0] == "首" and user_msg[1] == "先" and user_msg[2] == "是":
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你知道分手的原因嗎？\n分手的原因是......")
    )
    elif (len(user_msg) >= 7
      and user_msg[0] == "首"
      and user_msg[1] == "先"
      and user_msg[2] == "是"):
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你知道分手的原因嗎？\n分手的原因是......")
    )
    elif (len(user_msg) >= 7
      and user_msg[0] == "分"
      and user_msg[1] == "手"
      and user_msg[2] == "的"
      and user_msg[3] == "原"
      and user_msg[4] == "因"):
        textlist = []
        first_text = "一切都不容易對吧！儀式所需的道具基本集齊了，最後一個問題"
        sec_text = "如果你穿越時空回到過去，你和他初次約會的地方，你會想和那時候的自己說甚麼？"
        third_txt ="開頭：我想說......"
        textlist.append(TextSendMessage(first_text))
        textlist.append(TextSendMessage(sec_text))
        textlist.append(TextSendMessage(third_txt))
        line_bot_api.reply_message(
        event.reply_token,
        textlist
    )
    elif (len(user_msg) >= 7
      and user_msg[0] == "我"
      and user_msg[1] == "想"
      and user_msg[2] == "說"):
        image_carousel_template = ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url="https://i.ibb.co/1GBYvZn/image.png",
                  # Replace with your image URL
                action=MessageTemplateAction(label='Pray',text='Pray')
                
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
        
    

@line_handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id

    # Define Image Carousel Template
    image_carousel_template = ImageCarouselTemplate(
    columns=[
        ImageCarouselColumn(
            image_url="https://i.ibb.co/K7qPXfF/image.png",  # Replace with your image URL
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
    global working_status 
    msg = event.message.text
    
    if event.message.type != "text":
        return
    
    
    
    if event.message.text == "呼叫專員":
        working_status = True
        quick_reply = QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label="跟我聊聊", text="跟我聊聊")),
            QuickReplyButton(action=MessageAction(label="謝謝專員", text="謝謝專員"))
        ]
    )
        reply_message = TextSendMessage(text="請問有什麼需要協助的嗎?", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_message)
        
    if event.message.text == "跟我聊聊":
        working_status =True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="哈囉你好，請問您有什麼感情上的困擾嗎?"))
        return
    if event.message.text == "謝謝專員":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="歡迎再來找我"))
        return
    
    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
    


    user_message = event.message.text

    text_checker(event)

    if user_message == "Pray":
        working_status = False
        text_to_display = "一切即將結束"
        action_label = "超渡靈堂"
        action_text = "超渡靈堂"
        url_label = "超渡靈堂"
        url ="https://www.figma.com/proto/FmiYHeMnT5vqLzKovBTeSN/%E6%83%85%E6%84%9F%E8%91%AC%E5%84%80%E7%A4%BE-%E8%B6%85%E6%B8%A1%E9%9D%88%E5%A0%82?scaling=scale-down&page-id=0%3A1&node-id=56-2&starting-point-node-id=56%3A2"
        template_message = create_buttons_template_with_url(text_to_display,url_label, url, action_label, action_text)
        line_bot_api.push_message(
            event.source.user_id,
            template_message
        )

    if user_message == "大仇初報":
        working_status = False
        textlist = []
        first_text = "請您將剛剛調配的藥水擺在正前方，接下來的問題，如果您回答不出來，請拿攪拌棒滑過杯口一圈，並敲出清脆的一聲"
        sec_text = "必須滿足哪三個基本條件，你才覺得被愛？"
        third_txt ="首先是 ☐☐\n次要是 ☐☐\n一定要 ☐☐"
        textlist.append(TextSendMessage(first_text))
        textlist.append(TextSendMessage(sec_text))
        textlist.append(TextSendMessage(third_txt))
        line_bot_api.reply_message(
        event.reply_token,
        textlist
        )


    if user_message == "傳送":
        working_status = False
        text_to_display = "我們已將這句話傳達給那個您了，接下來請您移步報仇靈堂"
        action_label = "大仇初報"
        action_text = "大仇初報"
        url_label = "報仇靈堂"
        url ="https://www.figma.com/proto/pcov5Xttxuhh37z3nomXo1/%E6%83%85%E6%84%9F%E8%91%AC%E5%84%80%E7%A4%BE-%E5%A0%B1%E4%BB%87%E9%9D%88%E5%A0%82?type=design&node-id=1-2&t=PjcxbQRfMEq36a8n-0&scaling=scale-down&page-id=0%3A1&starting-point-node-id=1%3A2"
        template_message = create_buttons_template_with_url(text_to_display,url_label, url, action_label, action_text)
        line_bot_api.push_message(
            event.source.user_id,
            template_message
        )
    
        
    if user_message == "收下":
        working_status = False
        buttons_template = ButtonsTemplate(
            title=" ",
            text="現在請您看著台上正中間的杯子，其實杯子中的倒影正是那位被分手傷得極深的您，如果您能和她說話您想說什麼？",
            actions=[
                MessageTemplateAction(label="說完請按一下這裡", text="傳送"),
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
    if user_message == "世間美好":
        working_status = False
        buttons_template = ButtonsTemplate(
            title=" ",
            text="您應該記得剛剛抽到的善簽是甚麼顏色，請在中間的杯子抽一根一樣顏色的簽，請您收下這隻簽。",
            actions=[
                MessageTemplateAction(label="收下", text="收下"),
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
    if user_message == "Play":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="每個人在經歷被分手都會有不同的反應，因此請您思考一下自己的個性，選擇一個符合您自己的靈種，他將會映射出您自己。")
        )
        image_carousel_template = ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url="https://res.cloudinary.com/debk3y68m/image/upload/v1710601125/ntut/vzoc3cnbtr0g15g4ljio.png",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='怨靈',
                    text='怨靈'
                )
            ),
            ImageCarouselColumn(
                image_url="https://res.cloudinary.com/debk3y68m/image/upload/v1710601125/ntut/yyd2ix5esdz0xxacbxly.png",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='愁靈',
                    text='愁靈'
                )
            ),
            ImageCarouselColumn(
                image_url="https://res.cloudinary.com/debk3y68m/image/upload/v1710601125/ntut/uvmgdvrdg2tpksnswozl.png",  # 替換成您的圖片網址
                action=MessageTemplateAction(
                    label='損靈',
                    text='損靈'
                )
            ),
            
        ]
    )
        
    if user_message == "怨靈":
        working_status = False
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
        working_status = False
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
        working_status = False
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
        working_status = False
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
