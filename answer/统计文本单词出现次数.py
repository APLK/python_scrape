# encoding:utf-8
__author__ = 'APLK'
'''
任一个英文的纯文本文件，统计其中的单词出现的个数
'''
import io, re


def getCount():
    count = 0
    with io.open('E:\python_demo\hello\\answer\\0004.txt', 'r') as file:
        for line in file.readlines():
            allCount = re.findall("[a-zA-Z]+'*-*[a-zA-Z]+",line)
            count+=len(allCount)
    return count
print(getCount())
# count = 0
#
# with io.open('E:\python_demo\hello\\answer\\0004.txt', 'r') as file:
#     for line in file.readlines():
#         list = re.findall("[a-zA-Z]+'*-*[a-zA-Z]*", line)
#         count += len(list)
# print(count)