# encoding:utf-8
__author__ = 'APLK'
'''
你有一个目录，放了你一个月的日记，
都是 txt，为了避免分词的问题，
假设内容都是英文，请统计出你认为每篇日记最重要的词。
'''
import re, os, io

desDir = 'E:/python_demo/hello/answer/test'
list = {}
for file in os.listdir(desDir):
    if os.path.isfile(desDir + '/' + file):
        with io.open(desDir + '/' + file) as files:
            for line in files.readlines():
                findall = re.findall("[a-zA-Z]+'*-*[a-zA-Z]+", line)
                for word in findall:
                    word = word.lower()
                    if list.setdefault(word) is None:
                        list[word] = 1
                    else:
                        list[word] += 1
            print(str(list['the']))
# keywords = sorted(list, key=list.__getitem__, reverse=True)[0:5]
# print(keywords)

# 按照value进行排序
print(sorted(list.items(), key=lambda d: d[1],reverse=True)[0:3])


# firstWord=''
# temp=0
# for k,v in list.items():
#     # print(isinstance(v,int))
#     if v>=temp:
#         temp=v
#         firstWord=k
# print('出现最多的单词是:' + firstWord+',一共出现了%d次'%temp)
# test/China sends fresh water to Maldives.txt 中出现最多的是 water 出现了 9 次 ,其次是 the 出现了 9 次
# test/China's position paper on South China Sea.txt 中出现最多的是 the 出现了 69 次 ,其次是 of 出现了 36 次
# test/President Xi demands accelerated FTA strategy.txt 中出现最多的是 the 出现了 19 次 ,其次是 and 出现了 17 次
