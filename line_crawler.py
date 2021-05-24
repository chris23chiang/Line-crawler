
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,  StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('8w7Yod9eSIcC19Y2YpM1SGc46rc4OJhNQyC0ib/M9LBGRc6NFVwItlUGbOQ8M05R7vAEzazGEE6ehST2D692RR8h1RyZ1xE7banVgxBhieX/VWJeWjx6TvCiv4gq0uOAGKUqMtVZFBRovy1EzFl6hQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('36de434b16c6f81eebb94b8bf514b4ca')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    s = '很抱歉，您說什麼?'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )
        
        line_bot_api.reply_message(event.reply_token,sticker_message)
        return

    if msg in ['hi', 'Hi']:
        s = '嗨!'
    elif msg == '你吃飯了嗎':
        s = '還沒'
    elif msg == '你是誰':
        s = '我是機器人'
    elif '訂位' in msg:
        s = '你想訂位，是嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()