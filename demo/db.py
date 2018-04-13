#encoding:utf-8
import sqlite3

connect = sqlite3.connect('test1.db', 5000)
cursor = connect.cursor()
# cursor.execute('create table user (id int primary key,name varchar(20))')
# cursor.execute('insert into user(id,name) values(2,\'tom\')')
# cursor.execute('insert into user(id,name) values(3,\'lily\')')
# cursor.execute('DROP TABLE user')
cursor.execute('select * from user where name=(?)',('lily',))
print(cursor.fetchall())
cursor.close()
connect.commit()
connect.close()
