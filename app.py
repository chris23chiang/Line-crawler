# FOR TWM

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

#爬蟲的套件
import requests
from requests_html import HTML

# 計時器相關套件
import time
import datetime as dt

URL = 'https://www.ptt.cc/bbs/MobileComm/index.html' # 目標看板網址

def fetch(url): #把網頁的內容抓回來
    response = requests.get(url, cookies={'over18':'1'})
    return response

def parse_article_entries(doc): #用 requests_html 取 div.r-ent
    html = HTML( html = doc )
    post_entries = html.find('div.r-ent')
    return post_entries

def parse_article_meta(entry): #r-ent的內容格式化成 dict'
    meta = {
        'title': entry.find('div.title', first=True).text,
        'push': entry.find('div.nrec', first=True).text,
        'date': entry.find('div.date', first=True).text
    }
    try:
        # 正常的文章可以取得作者和連結
        meta['author'] = entry.find('div.author', first=True).text
        meta['link'] = entry.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        # 被刪除的文章我們就不要了
        meta['author'] = '[Deleted]'
        meta['link'] = '[Deleted]'
    return meta

def ptt_alert(url, keyword):
    url = url 
    resp = fetch(url) # 取得網頁內容
    post_entries = parse_article_entries(resp.text) # 取得各列標題

    for entry in post_entries:
        meta = parse_article_meta(entry)
        if keyword in meta['title'].lower() and not "截止" in meta['title']:
            s = '在「PTT手機討論版」發現關鍵字：「' + KEYWORD + '」！\n\n 標題：' + meta['title'] + ' \nhttps://www.ptt.cc' + meta['link']+'\n\n 人氣:' + meta['push']
            return s
            break
        else:
            continue
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='沒有搜尋到其他相關的文章，可輸入其他關鍵字試試看!')

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
    KEYWORD = event.message.text
    t = dt.datetime # 顯示時間用的
    s = ptt_alert(URL, KEYWORD)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))

if __name__ == "__main__":
    app.run()