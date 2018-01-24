import execjs
# with open('test')as f:
#     a=f.readlines()
# ctx=execjs.compile(a[0])
# print(ctx.call('SubTurnExport','http://kns.cnki.net/kns/ViewPage/viewsave.aspx','CJFD2009!SYSX200903028!1!0'))

import requests
a=requests.post('http://kns.cnki.net/kns/ViewPage/viewsave.aspx',data={'formfilenames':'CJFD2009!SYSX200903028!1!0'})
print(a.text.find('王倩'))