import requests as rq
from bs4 import BeautifulSoup
import time, json, argparse

#要抓：星座名稱、幸運時間、幸運星座、財運指數
#財運指數＋財運部分的敘述

def crawl(link):
    response = rq.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    dic = {}
    dic_constellation = {"10":"水瓶座", "11":"雙魚座", "0":"牡羊座", "1":"金牛座", "2":"雙子座", "3":"巨蟹座","4":"獅子座","5":"處女作",
     "6":"天秤座","7":"天蠍座","8":"射手座","9":"摩羯座"}
    
    #星座
    temp_index = link.find("Astro")
    dic["constellation"] = dic_constellation[link[temp_index+6]]
    
    #幸運時間
    dic["luc_time"]=soup.find_all("h4")[3].getText()
    
    #幸運星座
    dic["luc_constellation"]=soup.find_all("h4")[4].getText()
    
    #財運指數
    temp_index = str(soup.find_all("div", class_="STAR_LIGHT")[3]).find("icon") #找icon這個字樣
    fortune_index = str(soup.find_all("div", class_="STAR_LIGHT")[3])[temp_index+5]
    dic["fortune_index"] = fortune_index
    #財運部分描述
    fortune_descri = soup.find_all("span", class_="txt_orange")[0].parent.find_next_siblings("p")[0].getText()
    dic["fortune_descri"] = fortune_descri
    
    return dic

parser = argparse.ArgumentParser()
parser.add_argument('-web', type=str, help='website address')
args = parser.parse_args()

if __name__ == '__main__':
    output = crawl(args.web)
    #把title與document寫入
    print(output)
    jsObj = json.dumps(output, ensure_ascii=False)
    with open('./output.json', 'w') as f:
        f.write(jsObj)

