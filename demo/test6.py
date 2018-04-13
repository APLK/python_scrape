# encoding:utf-8
'''
@author:lk

@time:2017/9/15 

@desc:

'''


class Student:
    def __init__(self, *args):
        self.info = args;

    def print(self):
        print(repr(self.info))
        # print('name=' + self.info[0] + ',age=' + str(self.info[1]))


s1 = Student('lisi', 16);
s2 = Student('wangwu', 17);
s3 = Student('zhaoliu', 19);
l = [s1, s2, s3]
l = filter(lambda s: s.info[1] < 20, l)
while True:
    try:
        # 获得下一个值:
        x = next(l)
        x.print()
    except StopIteration:  # 遇到StopIteration就退出循环
        break





    # import functools

#
# def log(text):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kw):
#             print('%s %s():' % (text, func.__name__))
#             return func(*args, **kw)
#
#         return wrapper
#
#     return decorator
#
#
# def log1(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#
#     return wrapper
#
#
# @log('古典风格')
# def now():
#     print('2013-12-25')
#
#
# now1 = now()
# print(now.__name__)
