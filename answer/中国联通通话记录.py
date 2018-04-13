# encoding:utf-8
import re

__author__ = 'APLK'
'''
 登陆中国联通网上营业厅 后选择「自助服务」 --> 「详单查询」，然后选择你要查询的时间段，
 点击「查询」按钮，查询结果页面的最下方，点击「导出」，
 就会生成类似于 2014年10月01日～2014年10月31日通话详单.xls 文件。
 写代码，对每月通话时间做个统计。
'''
import xlrd
def getTime(file):
    workbook = xlrd.open_workbook(file)
    sheets_ = workbook.sheets()[0]
    nrows = sheets_.nrows
    minu=re.compile(r'([\d]+)分')
    second=re.compile(r'([\d]+)秒')
    timeMinuTotal=0
    timeSecondTotal=0
    for i in range(1,nrows):
        minu_findall = minu.findall(sheets_.cell(i, 3).value)
        second_findall = second.findall(sheets_.cell(i, 3).value)
        if len(minu_findall)==0:
            pass
        else:
            timeMinuTotal+= int(minu_findall[0])
        if len(second_findall)==0:
            pass
        else:
            timeSecondTotal+= int(second_findall[0])
    print(str(timeMinuTotal)+'分'+str(timeSecondTotal)+'秒')
    print(str(timeMinuTotal+timeSecondTotal//60)+'分'+str(timeSecondTotal%60)+'秒')
getTime('E:/python_demo/hello/answer/test/2017年08月语音通信.xls')