#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


gc = pygsheets.authorize(service_file='/Users/bnm41/ccCLUB2021/indigo-winter-315907-0edd187f4f0a.json')


# In[4]:


sht = gc.open_by_url(
'https://docs.google.com/spreadsheets/d/11s5hNH_TxdQwkaqUjCZucYEI1OcsLpAb_E2BNZynyJY/edit?fbclid=IwAR1WjSoOSjer4eMZ515XXB2hVuaV42RD3Ps6Rn2yuG1X701eyOFrP1n8XaA#gid=364565202')
wks = sht.worksheet_by_title("用戶輸入資訊")
Risk_Tolerance = int(wks.cell('C2').value)


# In[5]:


def stock_crawl(FL_ITEM0,FL_VAL_S0, FL_ITEM1,FL_VAL_S1,FL_SHEET,FL_SHEET2,FL_RULE0):
    #FL_VAL_S0 = 15
    #FL_VAL_S1 = 1700
    #FL_ITEM0 = "年度–ROE(%)"
    #FL_ITEM1 = "市值 (億元)"
    #FL_SHEET = 股價統計_歷年直接平均
    #FL_SHEET2 = 歷年總平均
    #FL_RULE0: 產業類別||金控業
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


# In[6]:


def screen(data):
    screen1 = data["股價  目前  落點"] == "近低" 
    screen2 = data["股價  目前  落點"] == "低" 
    screen3 = data["股價  目前  落點"] == "近高"
    #screen2 = data["PBR  目前  落點"] == "近低"
    weighted_stock_screen1 = data[screen1]
    weighted_stock_screen2 = data[screen2]
    weighted_stock_screen3 = data[screen3]
    weighted_stock_screen = pd.concat([weighted_stock_screen1, weighted_stock_screen2, weighted_stock_screen3])
    weighted_stock_screen_list = weighted_stock_screen[:]["名稱"].tolist()
    return weighted_stock_screen_list


# In[7]:


def screen1(data):
    screen1 = data["股價  目前  落點"] == "近低" 
    screen2 = data["股價  目前  落點"] == "低" 
    screen3 = data["股價  目前  落點"] == "近高"
    screen4 = data["成交"] >= 20
    weighted_stock_screen1 = data[screen1]
    weighted_stock_screen2 = data[screen2]
    weighted_stock_screen3 = data[screen3]
    weighted_stock_screen4 = data[screen4]
    weighted_stock_screen = pd.concat([weighted_stock_screen1, weighted_stock_screen2, weighted_stock_screen3,weighted_stock_screen4])
    weighted_stock_screen_list = weighted_stock_screen[:]["名稱"].tolist()
    return weighted_stock_screen_list


# In[8]:


def sheet(sheet,cell, stocks):
    wks2 = sht.worksheet_by_title(sheet)
    recommend_stocks = (" / ".join(stocks))
    wks2.update_value(cell , "推薦個股："＋recommend_stocks)


# In[125]:


if Risk_Tolerance == 1 :
    #金融股爬蟲 - 風險承受度低
    browser = webdriver.Chrome(ChromeDriverManager().install())
    data_holdings = stock_crawl("近四季–ROA(%)–本季度", 1, "市值 (億元)",0,"股價統計_歷年直接平均","近3年平均均","產業類別||金控業")
    data_banking = stock_crawl("近四季–ROA(%)–本季度", 1, "市值 (億元)",0,"股價統計_歷年直接平均","近3年平均","產業類別||銀行業")
    data_Finance = pd.concat([data_holdings, data_banking])
    Finance_stocks = screen(data_Finance)
    if len(Finance_stocks) != 0: 
        sheet("工作表2","A1", Finance_stocks)
    else:
        sheet("工作表2","A1", "今日無推薦個股")
        
    
elif Risk_Tolerance == 2 :
    #權值股爬蟲-風險承受度中
    browser = webdriver.Chrome(ChromeDriverManager().install())
    data = stock_crawl("年度–ROE(%)",15, "市值 (億元)",1700,"股價統計_歷年直接平均","近3年平均","")
    weighted_stocks = screen(data)
    if len(weighted_stocks) != 0:
        sheet("工作表2","A1", weighted_stocks)
    else:
        sheet("工作表2","A1", "今日無推薦個股")
        
        
elif Risk_Tolerance == 3 :
    #轉強股爬蟲 - 風險承受度高
    browser = webdriver.Chrome(ChromeDriverManager().install())
    data_strong = stock_crawl("當日：紅K棒棒幅(%)", 4, "單月營收年增減率(%)",20,"股價統計_歷年直接平均","近3年平均均","")
    data_strong = screen1(data_strong)
    if len(data_strong) != 0:
        sheet("工作表2","A1", data_strong)
    else:
        sheet("工作表2","A1", "今日無推薦個股")
        
else:
    print("輸入範圍錯誤，請輸入數字1~3")


# In[9]:


fortune_index = int(input())


# In[10]:


if  fortune_index == 1:
    balance = balance*0.4
    if Risk_Tolerance == 1:
        balance = balance*0.82
    elif Risk_Tolerance == 2:
        balance = balance*0.91
    elif Risk_Tolerance == 3:
        balance = balance*1
    else:
        print("輸入範圍錯誤")      
elif  fortune_index == 2:
    balance = balance*0.55
    if Risk_Tolerance == 1:
        balance = balance*0.82
    elif Risk_Tolerance == 2:
        balance = balance*0.91
    elif Risk_Tolerance == 3:
        balance = balance*1
    else:
        print("輸入範圍錯誤")  
elif  fortune_index == 3:
    balance = balance*0.75
    if Risk_Tolerance == 1:
        balance = balance*0.82
    elif Risk_Tolerance == 2:
        balance = balance*0.91
    elif Risk_Tolerance == 3:
        balance = balance*1
    else:
        print("輸入範圍錯誤")  
elif  fortune_index == 4:
    balance = balance*0.9
    if Risk_Tolerance == 1:
        balance = balance*0.82
    elif Risk_Tolerance == 2:
        balance = balance*0.91
    elif Risk_Tolerance == 3:
        balance = balance*1
    else:
        print("輸入範圍錯誤")  
elif  fortune_index == 5:
    balance = balance*1
    if Risk_Tolerance == 1:
        balance = balance*0.82
    elif Risk_Tolerance == 2:
        balance = balance*0.91
    elif Risk_Tolerance == 3:
        balance = balance*1
    else:
        print("輸入範圍錯誤")  

    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




