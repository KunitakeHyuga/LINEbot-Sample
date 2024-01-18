import os
from flask import Flask, abort, request
from linebot.v3.webhook import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = "DMg8NmxI9n9UM7d7k21uBYt5cg2bbhrp7diPgN8ZE5hUypMo90HWKDSvHstK7Fy+NjwK+rWY9nXDKTlsSM+ofeck4EggqxcQXlBoMojXKjot/fUM3qv7iJLEpzozMC1/3ud304szgER1ynYXrW3+ygdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "U883c49cc92f1e0a1b2de45aefafd3886"

handler = WebhookHandler('YOUR_CHANNEL_SECRET')
configuration = Configuration(access_token='YOUR_CHANNEL_ACCESS_TOKEN')

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        #相手の送信した内容で条件分岐して回答を変数に代入
        if event.message.text == 'グー':
            msg = 'パー'
        elif event.message.text == 'チョキ':
            msg = 'グー'
        elif event.message.text == 'パー':
            msg = 'チョキ'
        else:
            msg = 'ごめんね。\nまだ他のメッセージには対応してないよ'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

## 起動確認用ウェブサイトのトップページ
@app.route('/', methods=['GET'])
def toppage():
	return 'Hello world!'


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)