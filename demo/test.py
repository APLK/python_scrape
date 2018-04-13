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
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()


# 3.6
# Found mapping: id==><IntegerField:id>
# Found mapping: name==><StringField:username>
# Found mapping: email==><StringField:email>
# Found mapping: password==><StringField:password>
# SQL: insert into User (id,username,email,password) values (?,?,?,?)
# ARGS: [12345, 'Michael', 'test@orm.org', 'my-pwd']
# None
