# encoding:utf-8
'''
@author:lk

@time:2017/12/31 

@desc:

'''
# a = 10


def test():
    a = 50

    def test3():
        global a
        a = 100
        return a

    def test2():
        a = 60
        return a
    print(test3())
    print(test2())
    print(a)


test()
print(a)
