#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('indigo-winter-315907-0edd187f4f0a.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open('星流派投資魔法師')
ws = sh.worksheet('用戶輸入資訊') 


# In[8]:


def record_user_info(name, constellation, fortune_index, luc_time):
    id_lst = ws.col_values(1) 
    if name in id_lst: 
        id_cell = ws.find(name)
        constellation_cell = 'B'+ str(id_cell.row)
        fortune_index_cell = 'C'+ str(id_cell.row)
        lucy_time_cell = 'D'+ str(id_cell.row)
        ws.update(constellation_cell, constellation)
        ws.update(fortune_index_cell, fortune_index)
        ws.update(lucy_time_cell, luc_time)
         
    else:
        info = [name] + [constellation] + [fortune_index]+ [luc_time]
        ws.append_row((info)) 

def record_risk(name, info):
    id_cell = ws.find(name)
    risk_cell = 'E'+ str(id_cell.row)
    ws.update(risk_cell, info)    

def record_budget(name, info):
    id_cell = ws.find(name)
    budget_cell = 'F'+ str(id_cell.row)
    ws.update(budget_cell, info)      
    
def record_stock(name, info):
    id_cell = ws.find(name)
    stock_cell = 'G'+ str(id_cell.row)
    ws.update(stock_cell, info)    
    
def record_amount(name, info):
    id_cell = ws.find(name)
    amount_cell = 'H'+ str(id_cell.row)
    ws.update(amount_cell, info)    
    
    
    
#紀錄使用者id+星座+財運星數+幸運時間

#紀錄投資風險等級


#紀錄預算


#紀錄推薦個股
  

#紀錄建議下單金額



# In[9]:



def get_fortune_index(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 3).value 

def get_lucy_time(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 4).value 

def get_risk(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 5).value 

def get_budget(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 6).value 

def get_stock(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 7).value 

def get_amount(name):
    id_cell = ws.find(name)
    return ws.cell(id_cell.row, 8).value 



