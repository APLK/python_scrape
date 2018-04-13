# encoding:utf-8

# print "hello world"
# print 'hello','world1'
# name=raw_input("请输入名字:")
# print "hello,",name
# a=100
# if a>=1001:
#     print a
# else:
#     print -a
# print '''line1
# line2
#  ... line3'''
# print '\\\t\\n'
# print  ord('A')
# print  chr(65)
# a= u'中国,你好'.encode('utf-8')
# print a
# print '\xe4\xb8\xad'.decode('utf-8')
# print 'hello,%s'%'world'
# print 'the %s price is $%d.'%('egg',1000)
# print '%2d-%2d'%(3000,1)
# print '%.5f'%3.1415927
# print 'hello,%s%%' %u'黄种人'
# x=(2,)
# print len(x)
# print x
# if x:
#     print 'true'
# elif 0:
#     print '0'
# else:
#     print 'false'
# a=int(raw_input('you age:'))
# if a<10:
#     print '小学'
# else:
#     print '初中'

# print set([1,2,2,2,2,3])
# a=abs
# print a(-1)
# def getx(x, n=2):
#     s = 1
#     while n > 0:
#         n = n - 1
#         s = s * x
#     return s
#
#
# print getx(5)
#
#
# def isNone(n=[]):
#     # if n == None:
#     #     n = []
#     n.append('dgjgj')
#     return n
# print isNone()
# def fact(n):
#     return fact_1(n,1)
# def fact_1(num,product):
#     if num==1:
#         return product
#     return fact_1(num-1,num*product)
# print fact(100)
from collections import Iterable

# from os import listdir
# print [d for d in listdir('.')]

# a = {'a': 10, 'b': 20}
# b=123
# c='123'
# print isinstance(b, Iterable)
# print isinstance(c, Iterable)
# for key1, v in a.iteritems():
#     print key1, v
#
# print [x for x in range(0,10,4) if x%2==0]

# def fact(n):
#     a,b,c=0,0,1
#     while a<n:
#         yield c
#         b,c=c,b+c
#         a+=1
# print [n for n in fact(6)]
# print map(str,range(0,10))
# def firstUpper(str):
#     return str.lower()[0].upper()+str.lower()[1:]
# print map(firstUpper,['admin','LISA','barT'])
#
# def func1(n):
#     return n%2==1
# print filter(func1,range(0,10))
# f=lambda a:a*a
# print f(5)
# import functools
# def a(func):
#     @functools.wraps(func)
#     def b(*args,**kwargs):
#         print 'the func is %s'%func.__name__;
#         return func(*args,**kwargs)
#     return b
# @a
# def now():
#     print '2013.5.6'
#
# now()
#
# def d(text):
#     def e(func):
#         @functools.wraps(func)
#         def f(*args,**kwargs):
#             print '%s,%s'%(text,func.__name__)
#             return func(*args,**kwargs)
#         return f;
#     return e
# @d('log')
# def z():
#     print '20311'
# print d('djfjd')(z).__name__
#
# init2=functools.partial(int,base=3)
# print init2('100000')
# 'hell module'
# author = 'lldkf'
# import sys
#
#
# def test():
#     if len(sys.argv) == 1:
#         print ('hello,world.%s'%__name__)
#     elif len(sys.argv) == 2:
#         print ('hello, everybody'%__name__)
#     else:
#         print ('hello,nihao'%__name__)
#
#
# if __name__ == '__main__':
#     test()
# coding=utf-8
# from PIL import Image
# im=Image.open("E:\data_analyse.png")
# print (im.format,im.size,im.mode)
# b = im.convert("RGB")
# b.save("E:\\two.bmp")
# b.show()
# from types import MethodType
# class Dog(object):
#     def run(self):
#         print('Dog is running')
#
#
# class Cat(Dog):
#     def __init__(self):
#         self.x=10;
#     def __len__(self):
#         return 100
#
# cat = Cat();
# print(cat.__len__())
# print(len(cat))
# print(cat.x)
# print(hasattr(cat,'x'))
# print(getattr(cat,'x'))
# print(setattr(cat,'x',40))
# # print(setattr(cat,'sdfhsd',120))
# print(getattr(cat,'sdfhsd'))
# print(hasattr(cat,'sdfhsd'))
# def set_age(self,age):
#     self.age=age
#
#
# cat.set_age=MethodType(set_age,cat)
# cat.set_age(23)
# print(cat.age)

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            # for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            # for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__table__'] = name # 假设表名和类名一致
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        return type.__new__(cls, name, bases, attrs)

class Model(dict,metaclass=ModelMetaclass):
    # class Model(dict):
    #     __metaclass__ = ModelMetaclass
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            # for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
print(u.save())
