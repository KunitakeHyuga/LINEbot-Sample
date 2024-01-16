from flask import Flask, request, abort
import os
from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage,
    QuickReplyButton, QuickReply, PostbackAction, DatetimePickerAction
)

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "DMg8NmxI9n9UM7d7k21uBYt5cg2bbhrp7diPgN8ZE5hUypMo90HWKDSvHstK7Fy+NjwK+rWY9nXDKTlsSM+ofeck4EggqxcQXlBoMojXKjot/fUM3qv7iJLEpzozMC1/3ud304szgER1ynYXrW3+ygdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "U883c49cc92f1e0a1b2de45aefafd3886"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
parser = WebhookParser(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    push_text = event.message.text
    text = gcapi.extract_words(push_text)
    if text is None:
        text_message = TextSendMessage(text="Googleカレンダーの予定を知りたいですか？それとも追加したいですか？",
                                       quick_reply=QuickReply(items=[
                                           QuickReplyButton(action=DatetimePickerAction(
                                               label="予定を知りたい", data="read", mode="date")),
                                           QuickReplyButton(action=PostbackAction(
                                               label="予定を追加したい", data="write"))
                                       ]))
        line_bot_api.reply_message(event.reply_token, text_message)
    else:
        htmllink = gcapi.write(*text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=htmllink))

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == "read":
        date = event.postback.params['date']
        msg = gcapi.read(date)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    elif event.postback.data == "write":  # 修正した箇所
        text_write = "以下の形式で追加したい予定を入力してください。"\
                     "入力形式が正しくない場合、最初のクイックリプライに戻ります。追加に成功した場合はURLが表示されます。"\
                     "\n予定名\n場所(任意)\n年月日(半角数字8桁)\n開始時間(半角数字4桁)\n終了時間(半角数字4桁)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text_write))

if __name__ == "__main27__":
    port = int(os.getenv("PORT", 5000))  # デフォルトのポートを指定
    app.run(host="0.0.0.0", port=port)
