
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()