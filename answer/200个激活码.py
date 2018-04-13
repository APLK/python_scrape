# encoding:utf-8
__author__ = 'APLK'
'''
1.生成 200 个激活码（或者优惠券）
2.保存到 MySQL 关系型数据库中
3.保存到 Redis 非关系型数据库中
'''

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import pymysql


def get200Code(num):
    while num > 0:
        newIm = Image.new('RGB', (240, 60), color=(255, 255, 255))
        font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 30)
        draw = ImageDraw.Draw(newIm)
        for x in range(0, 240):
            for y in range(0, 60):
                draw.point((x, y), fill=(
                    random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)))
        numStr = ''
        for x in range(0, 4):
            s = chr(random.randint(65, 90))
            draw.text((x * 60 + 12, 10), chr(random.randint(65, 90)), fill=(
                random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)),
                      font=font)
            numStr += str(s)
        saveSql(numStr,num)
        im_filter = newIm.filter(ImageFilter.BLUR)
        im_filter.save('E:\python_demo\hello\\answer\\code' + str(num) + '.png', 'png')
        num = num - 1


def saveSql(numStr,x):
    TABLENAME = 'CODETABLE'
    TABLE_ID = 'TABLE_ID'
    TABLE_NAME = 'TABLE_NAME'
    DATA_NAME = 'codedb'
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456',
                               charset='utf8')
    cursor = conn.cursor()
    cursor.execute('create database if not exists ' + DATA_NAME)
    cursor.execute("use "+ DATA_NAME)
    if x==10:
        delete="DROP TABLE IF EXISTS %s"%TABLENAME
        cursor.execute(delete)
        # DELETESQL="DELETE FROM %s WHERE %s>%d"%(TABLENAME,TABLE_ID,0)
        # cursor.execute(DELETESQL)
    CREATESQL =  "CREATE TABLE IF NOT EXISTS %s (%s int NOT NULL PRIMARY KEY AUTO_INCREMENT,%s CHAR(30) NOT NULL unique)" %(TABLENAME,TABLE_ID,TABLE_NAME)
    INSERTSQL = "INSERT INTO %s(%s) VALUES('%s')"%(TABLENAME,TABLE_NAME,numStr)
    QUERYSQL = "SELECT * FROM %s"%TABLENAME
    cursor.execute(CREATESQL)
    cursor.execute("Alter table %s AUTO_INCREMENT=0"%TABLENAME)
    cursor.execute(INSERTSQL)
    cursor.execute(QUERYSQL)
    conn.commit()
    conn.rollback()
    cursor.close()
    conn.close()


# 生成验证码
get200Code(10)

db_host = ''
db_user = ''
db_pw = ''
db_name = 'vdt'
