#!/usr/bin/env python
# coding: utf-8

# In[1]:


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






# In[4]:


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


# In[5]:


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


# In[6]:


def screen1(data):
    screen1 = data["股價  目前  落點"] == "近低" 
    screen2 = data["股價  目前  落點"] == "低" 
    screen3 = data["股價  目前  落點"] == "近高"
    weighted_stock_screen1 = data[screen1]
    weighted_stock_screen2 = data[screen2]
    weighted_stock_screen3 = data[screen3]
    weighted_stock_screen = pd.concat([weighted_stock_screen1, weighted_stock_screen2, weighted_stock_screen3])
    weighted_stock_screen_list = weighted_stock_screen[:]["名稱"].tolist()
    return weighted_stock_screen_list


# In[7]:





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




