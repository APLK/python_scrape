# encoding:utf-8
__author__ = 'APLK'
'''
1.敏感词文本文件 filtered_words.txt，里面的内容为以下内容，
当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。
2.敏感词文本文件 filtered_words.txt，里面的内容 和 0011题一样，当用户输入敏感词语，则用 星号 * 替换，
例如当用户输入「北京是个好城市」，则变成「**是个好城市」。
'''

import io

with io.open('E:/python_demo/hello/answer/test/filtered_words.txt', 'rb') as file:
    read = str(file.read(), encoding='utf-8').split('\n')
    while True:
        word = input("请输入词汇:")
        if word == 'quit':
            break
        for value in word:
            print(value)
            if value in read:
                pass
            else:
                print('词汇合法')
                break
        else:
            print('词汇不合法')
            # flag=True
            # isFiltered=False
            # while flag:
            #     int_put = input('请输入文字:')
            #     for f in read:
            #         if int_put.find(f) != -1:
            #             isFiltered=True
            #         elif int_put=='quit':
            #             flag=False
            #             break
            #         else:
            #             isFiltered=False
            #     if isFiltered:
            #         print('Freedom')
            #     else:
            #         print('Human Rights')

        # with open('E:/python_demo/hello/answer/test/filtered_words.txt', 'rb') as f:
        #     data = f.read()
        #
        # filt = str(data, encoding="utf-8").split('\n')
        #
        # while True:
        #     text = input("please input:")
        #     for x in filt:
        #         if text.find(x) != -1:
        #             text = text.replace(x, '*' * len(x))
        #     print(text)

        # 北京,程序员,公务员,领导,牛比,牛逼,你娘,你妈,love,sex,jiangge
