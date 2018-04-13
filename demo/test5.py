#encoding:utf-8
import urllib.request
import time
import re
print(time.clock())
url='http://sz.lianjia.com/ershoufang/pg'
for x in range(2):
    finalUrl=url+str(x)+'/'
    res=urllib.request.urlopen(url).read()
    content = res.decode('utf-8')
    result=re.findall(r'>.{1,100}?</div></div><div class="flood">',content)
    print(x)
    for i in result:
        print(i[0:-31].replace('</a>',''))
        # print(bytes((i[0:-31].replace('</a>','')),encoding='utf-8').decode('utf-8'))
print(time.clock())
