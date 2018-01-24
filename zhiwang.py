import requests
import time
from urllib.parse import urlencode
import scrapy
import re
import os
# 不带r系统会觉得\U是编码声明
keylist=os.listdir(r'C:\Users\hp\Desktop\文献、\综述')
for k in keylist:
    key=k.strip('.pdf').split('_')[0]
    try:
        author=k.strip('.pdf').split('_')[1]
    except:
        author=''
    # key="氯化1_甲基_3_丁基咪唑的制备与表征"
    # 不带cookie的请求头，从chrome复制的
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"nvsm.cnki.net",
        "Referer":"http://nvsm.cnki.net/kns/brief/default_result.aspx",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    }
    # searchHandler的post参数
    formdata_searchHandler={
        "action":"",
        "NaviCode":"*",
        "ua":"1.11",
        "isinEn":"1",
        "PageName":"ASP.brief_default_result_aspx",
        "DbPrefix":"SCDB",
        "DbCatalog":"中国学术文献网络出版总库",
        "ConfigFile":"SCDBINDEX.xml",
        "db_opt":"CJFQ,CJRF,CDFD,CMFD,CPFD,IPFD,CCND,CCJD",
        "txt_1_sel":"SU$%=|",
        "txt_1_value1":key,
        "txt_1_special1":"%",
        "his":"0",
        "parentdb":"SCDB",
    }
    # Session可以保持请求的状态，保持不同请求之间cookie沿用相同的cookie
    s=requests.Session()
    # post请求之后服务器才有用户的记录，否则无法获得搜索结果列表，说用户不存在
    bb=s.post('http://nvsm.cnki.net/kns/request/SearchHandler.ashx',data=formdata_searchHandler,headers=headers)
    # brief里是搜索结果
    url='http://nvsm.cnki.net/kns/brief/brief.aspx?'
    parameter={
        "pagename":"ASP.brief_default_result_aspx",
        "isinEn":"1",
        "dbPrefix":"SCDB",
        "dbCatalog":"中国学术文献网络出版总库",
        "ConfigFile":"SCDBINDEX.xml",
        "research":"off",
        "t":int(time.time()),
        "keyValue":key,
        "S":"1",
        "sorttype":"(FFD,'RANK') desc",
    }
    # 用urlencode构建网址
    search=s.get(url+urlencode(parameter),headers=headers)
    selector=scrapy.Selector(text=search.text)
    # 仅仅<tbody>无法被找到
    d_url=selector.xpath('//table[@class="GridTableContent"]/tr[2]/td[2]/a/@href').extract_first()
    # 修改获得的网址，使得可以正常访问链接
    d_url=d_url.replace('/kns','http://kns.cnki.net/KCMS')
    search=s.get(d_url)
    selector=scrapy.Selector(text=search.text)
    # 导出参考文献是一个js函数，有两个参数 网址和文件名，点击会在新建标签页打开新的网址
    cankao=selector.xpath('//div[@class="wxTitle"]/div[@class="link"]/a[1]/@onclick').extract_first()
    # 把网址和文件名分开，之前用，连接。search函数需要group（）
    caokao_url=re.search(r'\'.*\'',cankao).group().split(',')
    # 获得的网址和文件名带单引号，去掉。用fiddle抓包发现新建的标签页是post请求的
    search=s.post(caokao_url[0].strip('\''),data={'formfilenames':caokao_url[1].strip('\'')})
    selector=scrapy.Selector(text=search.text)
    # 仅仅<tr>用xpath无法识别，可以直接忽略
    # text=selector.xpath('//table[@class="mainTable"]/tr[1]/td/text()').extract_first()
    text=selector.xpath('//table[@class="mainTable"]/td[1]/text()').extract_first()
    # 输出参考文献
    print(text)
