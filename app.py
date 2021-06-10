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

####修改的###
from Stock_market_crawler import screen ,screen1
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from pyquery import PyQuery as pq
from time import sleep
from sklearn.datasets import make_classification
import pygsheets
from database_functions import  get_fortune_index,get_risk,get_budget,record_stock,record_amount

def stock_crawl(FL_ITEM0,FL_VAL_S0, FL_ITEM1,FL_VAL_S1,FL_SHEET,FL_SHEET2,FL_RULE0):

    my_params = {"MARKET_CAT": "自訂篩選", "INDUSTRY_CAT": "我的條件", "FL_ITEM0" : FL_ITEM0 , "FL_VAL_S0" :FL_VAL_S0 ,              "FL_ITEM1": FL_ITEM1 ,"FL_VAL_S1": FL_VAL_S1, "FL_SHEET": FL_SHEET , "FL_SHEET2": FL_SHEET2,"FL_RULE0": FL_RULE0}
    
    url = 'https://goodinfo.tw/StockInfo/StockList.asp?'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36' }

    #請求網站
    list_req = requests.get(url, headers = headers,  params = my_params )
    browser.get(list_req.url)
    query_button = browser.find_element_by_css_selector("#MENU10 > tbody > tr:nth-child(2) > td > form > table > tbody > tr:nth-child(19) > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > nobr > input[type=submit]")
    query_button.click()
    sleep(0.5)
    #list_button_ = browser.find_element_by_css_selector("#selSHEET").click()
    #sleep(0.5)
    #stoavg_button = browser.find_element_by_css_selector("#selSHEET > option:nth-child(number)".replace("number",str(num))).click()
    #sleep(15)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    table = soup.find('table', {'id': 'tblStockList'})
    df = pd.read_html(table.prettify())
    df = df[0]
    df.columns = df.columns.get_level_values(-1)
    df.columns = df.iloc[0]
    a = df[df['名稱'].isin(["名稱"])].index
    df = df.drop(a)
    
    return df
####修改的###


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
        buttons_template = ButtonsTemplate(
            title='魔法師咒語', text='請選擇星座', actions=[
                MessageAction(
                    label='牡羊座',
                    text='牡羊座'
                )
            ])
        """
        MessageAction(
            label='金牛座',
            text='金牛座'
        ),
        MessageAction(
            label='雙子座',
            text='雙子座'
        ),
        MessageAction(
            label='巨蟹座',
            text='巨蟹座'
        ),
        MessageAction(
            label='獅子座',
            text='獅子座'
        ),
        MessageAction(
            label='處女座',
            text='處女座'
        ),
        MessageAction(
            label='天秤座',
            text='天秤座'
        ),
        MessageAction(
            label='天蠍座',
            text='天蠍座'
        ),
        MessageAction(
            label='射手座',
            text='射手座'
        ),
        MessageAction(
            label='摩羯座',
            text='摩羯座'
        ),
        MessageAction(
            label='水瓶座',
            text='水瓶座'
        ),
        MessageAction(
            label='雙魚座',
            text='雙魚座'
        )
        """
            
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template) #alt_text為無法輸出時產生的字樣
        line_bot_api.reply_message(event.reply_token, template_message)





    if text == "天蠍座":
        website_address = "https://astro.click108.com.tw/daily_7.php?iAstro=7#lucky"
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "水瓶座":
        website_address = "https://astro.click108.com.tw/daily_10.php?iAstro=10&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "雙魚座":
        website_address = "https://astro.click108.com.tw/daily_11.php?iAstro=11&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "牡羊座":
        website_address = "https://astro.click108.com.tw/daily_0.php?iAstro=0&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "金牛座":
        website_address = "https://astro.click108.com.tw/daily_1.php?iAstro=1&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "雙子座":
        website_address = "https://astro.click108.com.tw/daily_2.php?iAstro=2&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "巨蟹座":
        website_address = "https://astro.click108.com.tw/daily_3.php?iAstro=3&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "獅子座":
        website_address = "https://astro.click108.com.tw/daily_4.php?iAstro=4&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "處女座":
        website_address = "https://astro.click108.com.tw/daily_5.php?iAstro=5&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "天秤座":
        website_address = "https://astro.click108.com.tw/daily_6.php?iAstro=6&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "射手座":
        website_address = "https://astro.click108.com.tw/daily_8.php?iAstro=8&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)

    elif text == "摩羯座":
        website_address = "https://astro.click108.com.tw/daily_9.php?iAstro=9&Type=0&iAcDay=" + time.strftime('%Y-%m-%d+1', time.localtime())
        dic_constellation = crawl(website_address)
                
        message = TextSendMessage(text="今天財運描述: \n"+dic_constellation["fortune_descri"])
        line_bot_api.push_message(user_id, message)

        if int(dic_constellation["fortune_index"]) >= 3:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天您適合投資喔！想繼續看下去的話，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
        if int(dic_constellation["fortune_index"]) <= 2:
            message = TextSendMessage(text="今天財運指數: \n"+dic_constellation["fortune_index"]+"顆🌟" + "今天的運勢不太適合投資呢，若仍想繼續看下去，請打：財運滾滾來")
            line_bot_api.push_message(user_id, message)
    
    elif text == "財運滾滾來":
            message = TextSendMessage(text="請輸入您的風險承受度，如：風險高 / 如：風險中 / 如：風險低，讓魔法師給你最佳投資建議")
            line_bot_api.push_message(user_id, message)

    else:
        buttons_template = ButtonsTemplate(
            title='Button Template', text='下面有不同功能的button', actions=[
                URIAction(label='好看的影片喔^^', uri='https://www.youtube.com/watch?v=072tU1tamd0'),
                MessageAction(label='想要再玩一次', text='開始')#幫用戶說一段指定訊息
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template) #alt_text為無法輸出時產生的字樣
        line_bot_api.reply_message(event.reply_token, template_message)
     

#請接著這裡寫下去
####修改的###
    #Risk_Tolerance =  int(get_risk(user_id))
    #if Risk_Tolerance == 1 :
    if text == "風險低":
        Risk_Tolerance == 1 
        #金融股爬蟲 - 風險承受度低
        browser = webdriver.Chrome(ChromeDriverManager().install())
        data_holdings = stock_crawl("近四季–ROA(%)–本季度", 1, "市值 (億元)",0,"股價統計_歷年直接平均","近3年平均均","產業類別||金控業")
        data_banking = stock_crawl("近四季–ROA(%)–本季度", 1, "市值 (億元)",0,"股價統計_歷年直接平均","近3年平均","產業類別||銀行業")
        data_Finance = pd.concat([data_holdings, data_banking])
        Finance_stocks = screen(data_Finance)
        if len(Finance_stocks) != 0: 
            #record_stock(user_id, " / ".join(Finance_stocks))
            message = TextSendMessage(text= " / ".join(Finance_stocks))
            line_bot_api.push_message(user_id, message)

        else:
            #record_stock(user_id, "今日無推薦個股")
            message = TextSendMessage(text= "今日無推薦個股")
            line_bot_api.push_message(user_id, message)



    #elif Risk_Tolerance == 2 :
    elif text == "風險中":
        Risk_Tolerance == 2
        #權值股爬蟲-風險承受度中
        browser = webdriver.Chrome(ChromeDriverManager().install())
        data = stock_crawl("年度–ROE(%)",15, "市值 (億元)",1700,"股價統計_歷年直接平均","近3年平均","")
        weighted_stocks = screen(data)
        if len(weighted_stocks) != 0:
            #record_stock(user_id, " / ".join(weighted_stocks))
            message = TextSendMessage(text= " / ".join(weighted_stocks))
            line_bot_api.push_message(user_id, message)
        else:
            #record_stock(user_id, "今日無推薦個股")
            message = TextSendMessage(text= "今日無推薦個股")
            line_bot_api.push_message(user_id, message)


    #elif Risk_Tolerance == 3 :
    if text == "風險高":
        Risk_Tolerance == 3
        #轉強股爬蟲 - 風險承受度高
        browser = webdriver.Chrome(ChromeDriverManager().install())
        data_strong = stock_crawl("當日：紅K棒棒幅(%)", 4, "單月營收年增減率(%)",20,"股價統計_歷年直接平均","近3年平均均","")
        data_strong = screen1(data_strong)
        if len(data_strong) != 0:
            #record_stock(user_id, " / ".join(data_strong))
            message = TextSendMessage(text= " / ".join(data_strong))
            line_bot_api.push_message(user_id, message)
        else:
            #record_stock(user_id, "今日無推薦個股")
            message = TextSendMessage(text= "今日無推薦個股")
            line_bot_api.push_message(user_id, message)
####修改的###

  

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
