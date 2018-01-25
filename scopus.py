import requests
import scrapy
from urllib.parse import urlencode
import os
keylists=os.listdir(r'C:\Users\hp\Desktop\文献、\乙二醇')
for k in keylists:
    key=k.strip('.pdf')
    # 基本网页
    basic=requests.get('https://www.scopus.com/search/form.uri?display=basic')
    selector=scrapy.Selector(text=basic.text)
    # 获取请求参数
    sid=selector.xpath('//*[@id="sid"]/@value').extract_first()
    txGid=selector.xpath('//*[@id="txGid"]/@value').extract_first()
    searchId=selector.xpath('//*[@id="searchId"]/@value').extract_first()
    # 构造请求参数
    # key="Catalytic performance of metal oxides for the synthesis of propylene carbonate from urea and 1,2-propanediol"
    parametal={
        "numberOfFields":"0",
        "src":"s",
        "clickedLink":"",
        "edit":"",
        "editSaveSearch":"",
        "origin":"searchbasic",
        "authorTab":"",
        "affiliationTab":"",
        "advancedTab":"",
        "scint":"1",
        "menu":"search",
        "tablin":"",
        "searchterm1":key,
        "field1":"TITLE_ABS_KEY",
        "dateType":"Publication_Date_Type",
        "yearFrom":"Before 1960",
        "yearTo":"Present",
        "loadDate":"7",
        "documenttype":"All",
        "resetFormLink":"",
        "st1":key,
        "st2":"",
        "sot":"b",
        "sdt":"b",
        "sl":"123",
        "s":"TITLE-ABS-KEY({})".format(key),
        "sid":sid,
        "searchId":searchId,
        "txGid":txGid,
        "sort":"r-f",
        "originationType":"b",
        "rr":"",
    }
    url='https://www.scopus.com/results/results.uri?'
    result=requests.get(url+urlencode(parametal))
    selector=scrapy.Selector(text=result.text)
    # 获取文献信息
    info=selector.xpath('//*[@id="resultDataRow0"]/td').xpath('string(.)').extract()
    # 作者，年份，标题，期刊名字，卷_期，页范围
    try:
        author=info[1].strip()
        year=info[2].strip()
        title=info[0].strip()
        journal=info[3].strip().split('\n')[0]
        vol_issue=info[3].strip().split('\n')[1]
        page=info[3].strip().split('\n')[3]
        cankao='{}{}[J].{},{},{}:{}.'.format(author,title,journal,year,vol_issue,page)
    except:
        cankao='查找出错 文件名为:{}'.format(key)
    print(cankao)