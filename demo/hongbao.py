# encoding:utf-8
'''
@author:lk

@time:2018/1/17 

@desc:

'''


# -*- coding: cp936 -*-
# 函数实际就是这样的
def set_fun():
    fs = []
    # lamda x:x*i for i in range(4)的实质如下,
    # 此处的i实际上是个全局变量,每次调用lamda(x)函数时并没绑定i的值,
    #函数首先会循环for 4次将lamda函数添加到fs中,执行完后i=3,此时
    #函数返回了fs,fs中存的是lamda函数,所以此时会引用内部函数,这时候内部函数就会调用
    # 外部函数的i=3变量,这时候lamda函数才是3x
    # 直到循环结束i变为了3时才将i=3的值赋给了lamda(x)函数中的i,
    # 所以fs的数组值就是[3x,3x,3x,3x]
    # 外部函数的i全局变量会被lamda(x)内部函数调用
    for i in range(4):
        def lamda(x):
            return x * i
        fs.append(lamda)
    # set_fun()函数的返回值会被内部函数lamda引用
    return fs


# set_fun()函数返回的值就是fs数组
# 当for循环fs数组时需要传递一个x变量给内部函数lamda(x),此时传了3
# 所以打印的结果就是9,9,9,9
for ev in set_fun():
    print(ev(3))


# f=[lambda x,i=i:x*i for i in range(4)]
# print(f[0](3))
# print(f[1](3))
# print(f[2](3))

# import random
#
#
# def checkparam(num):
#     if (type(num) != type(1)):
#         print('num must be Integer')
#         return False;
#     if (num < 0):
#         print('num must be Positive Integer')
#         return False;
#     return True;
#
#
# def roll(total, num, float_num):
#     print('共', total, '。分', num, '份。条件参数为：', float_num)
#     if (checkparam(num)):
#         p = []
#         average = total / num
#         print('下浮值: ', str(int(average) - float_num), ',上浮值: ' + str(int(average) + float_num))
#         divlist = []
#         # 份数
#         for count in range(0, num):
#             # 从average - float_num到average + float_num中随机产生一个值
#             randnumber = random.randint(int(average) - float_num, int(average) + float_num)
#             divlist.append(randnumber)
#         print('随机数列为: ', divlist, ' 长度为: ', str(len(divlist)))
#         sumdiv = sum(divlist)
#         print(num, '份的随机数组总值为: ' + str(sumdiv))
#         # 四舍五入的比例值,2是小数点位数
#         scale = round(total / sumdiv, 2)
#         print('-------')
#         # 循环num-1次
#         for m in range(0, len(divlist) - 1):
#             # 计算每一份在total中所占的比例
#             randnumber = round(scale * divlist[m], 2)
#             if randnumber>int(average) + float_num:
#                 randnumber=int(average) + float_num
#             if randnumber<int(average) - float_num:
#                 randnumber=int(average) - float_num
#             p.append(randnumber)
#         sumtp = sum(p)
#         print('前', str(num - 1), '份的总值: ' + str(round(sumtp, 2)))
#         # 最后一份就用总数减掉
#         last = round(total - sumtp, 2)
#         print('最后一份的值: ' + str(last))
#         p.append(last)
#         print('结果中其中最大的值为: ', str(sorted(p)[num - 1]), '最小值为: ' + str(sorted(p)[0]))
#         print('满足条件的结果数列为: ', p, ' 长度为: ', str(len(p)))
#         print('结果数列的总值为: ', str(round(sum(p), 2)))
#
#
# # 总金额，份数，调控参数（调控上下浮动值）
# roll(100, 8, 6)
