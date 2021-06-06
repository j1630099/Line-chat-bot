from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Z9wIs5xSAOaOPM8LoQz0pv/Tw9PoP0Ph2se6h1RlUEB0uSTKoRwBwSIJ0YQZ/9YWAneVWI5XQoAWuL5lkD2UEeuzhvMUlYZy+Re3psIaEyOAvtKPnrBCCp7OwM07CVWYSj1P/06bIRPxtY/Bp3whuAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('ef72f810af4eee6fed399eae10ca7c10')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #text = event.message.text

    """
    設計邏輯：
    沒辦法再這個function直接設計一套流程，且也沒辦法儲存variable(除非用database)

    先問星座, 並且問平常傾向哪一種投資
    然後下一次reply, 再一次回應
    """
    text=event.message.text
    user_id = event.source.user_id
    if text == "開始":
        temp_text = "請問你的星座，以及你是風險低中高者（以數3,2,1）代表"
        message = TextSendMessage(text=temp_text)
        line_bot_api.push_message(user_id, message)  

    elif text == "天蠍座 1":
        """
        把爬蟲弄進來，根據運勢去做篩選
        """
        message = TextSendMessage(text="投資投資")
        line_bot_api.push_message(user_id, message)
    
    elif text == "風險高":
        """
        根據風險，做投資組合推薦
        """
        pass
    else:
        message = TextSendMessage(text="閉嘴")
        line_bot_api.push_message(user_id, message)
        pass
    
    #line_bot_api.reply_message(event.reply_token, message)
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
