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




