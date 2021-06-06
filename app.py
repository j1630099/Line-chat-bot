from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from crawl_constellation import crawl
import time

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('76WUlkR2tplP1B2UcokpbtLwvPqOLPaVinGlKOZa5Q3rsZ1c+EPPSQkGVNXsGCqIPuf0XykI0SZeiul8L1YJeHnusR3efcr9EWwkthn++GRkWShrjCblyMCuBimcDrxQ1YgLQsHAatSUseiM+Yw6KgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8b60532b9cadf514f5d0c72006d3ccf9')

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


#資料庫的部分
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

def record_user_text(info):
    # 這段是憑證認證的標準作業
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('indigo-winter-315907-0edd187f4f0a.json', scope)
    gc = gspread.authorize(credentials)

    # 選擇試算表
    sh = gc.open('星流派投資魔法師')

    # 選擇要開始編輯的工作表
    ws = sh.worksheet('用戶輸入資訊')
    
    #在工作表新增一列, 存入使用者的資訊
    ws.append_row((info))




# 處理訊息  ＃以下確認要不要用 Reply
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text=event.message.text
    user_id = event.source.user_id
    if text == "開始":
        temp_text = "歡迎來到星流派投資魔法師，想抓住財富跟幸運，就請告訴我您的星座吧～（輸入格式：ＸＸ座) "
        message = TextSendMessage(text=temp_text)
        line_bot_api.push_message(user_id, message)  

    elif text == "天蠍座":
        website_address = "https://astro.click108.com.tw/daily_10.php?iAstro=8&iAcDay=" + time.strftime('%Y-%m-%d', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"])
        line_bot_api.push_message(user_id, message)
        
    
    else:
        message = TextSendMessage(text="輸入錯誤")
        line_bot_api.push_message(user_id, message)
        pass

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
