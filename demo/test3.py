# encoding:utf-8
# import re
# import itertools
# re1=re.match(r'^\d{3}\-\d{3,8}$','012-51542244')
# if re1:
#     print('match success')
# else:
#     print('match error')
#
# print(re.split(r'\s+','a b   c'))
# print(re.match(r'^(\d{3})-(\d{3,8})$','012-58745').groups())
# print(re.match(r'^(\d*?)(0{2,})(.*?)$','1023000001fg2001').groups())
# a=itertools.starmap(lambda x:x*x,itertools.count(1))
# b=map(lambda x:x*x,[1,2,3])
# print(a)
# print(b)
# for n in itertools.takewhile(lambda x:x<100,a):
#     print(n)

# from xml.parsers.expat import ParserCreate
#
# class DefaultSaxHandler1(object):
#     def start_et(self,name,attrs):
#         print('sax:start_element: %s,attrs: %s' % (name,str(attrs)))
#
#     def end_et(self, name):
#         print('sax:end_element: %s' % name)
#
#     def char_et(self, text):
#         print('sax:char_data : %s' % text)
#
# xml = r'''<?xml version= "1.0"?>
#
#
# <ol>
#         <li><a href = "/python">Python</a></li>
#         <li><a href = "/ruby">Ruby</a></li>
# </ol>
#
#
# '''
#
# handler = DefaultSaxHandler1()
# parser = ParserCreate()
#
# # parser.returns_unicode = True
# parser.StartElementHandler = handler.start_et
# parser.EndElementHandler = handler.end_et
# parser.CharacterDataHandler = handler.char_et
# parser.Parse(xml)

# from HTMLParser import HTMLParser
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print('handle_starttag<%s>,content:%s' % (tag,str(attrs)))
#     def handle_endtag(self, tag):
#         print('handle_endtag</%s>' % tag)
#     def handle_startendtag(self, tag, attrs):
#         print('handle_startendtag<%s/>,content:%s'  % (tag,str(attrs)))
#     def handle_data(self, data):
#         print('handle_data:%s'%data)
#     def handle_comment(self, data):
#         print('<!-- -->')
#     def handle_entityref(self, name):
#         print('handle_comment:&%s;' % name)
#     def handle_charref(self, name):
#         print('handle_comment:&#%s;' % name)
# parser = MyHTMLParser()
# parser.feed('<html><head></head><body><p>Some <a href=\"#\">html</a> tutorial...<br>END</p></body></html>')
# from PIL import Image,ImageDraw,ImageFilter,ImageFont
# import random
# def rndChar():
#     return chr(random.randint(65,90))
# def rndColor():
#     return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
# def rndColor2():
#     return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
# width=240
# height=60
# img = Image.new('RGB', (width, height), (255,255,255))
# draw = ImageDraw.Draw(img)
# font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
# for x in range(width):
#     for y in range(height):
#         draw.point((x,y),fill=rndColor())
# for n in range(4):
#     draw.text((n*60+10,10),rndChar(),fill=rndColor2(),font=font)
# img_filter = img.filter(ImageFilter.BLUR)
# img_filter.save('D:/test.jpg','jpeg')
# from PIL import Image,ImageFilter,ImageFont,ImageDraw
# import random
# def rndChar():
#     return chr(random.randint(65,90))
# def rndColor():
#     return (random.randint(64,255),random.randint(64,255),random.randint(64,255))
# def rndColor2():
#     return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
# width=240
# height=60
# img = Image.new('RGB', (width, height), (255, 255, 255))
# draw = ImageDraw.Draw(img)
# font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
# for x in range(width):
#     for y in range(height):
#         draw.point((x,y),fill=rndColor())
# for n in range(4):
#     draw.text((n*60+10,10),rndChar(),fill=rndColor2(),font=font)
# img_filter = img.filter(ImageFilter.BLUR)
# img_filter.save('D:/test2.jpg','jpeg')
# def fn(n):
#     count=0
#     for n in range(1,n):
#         if n%7==0:
#             count=count+1
#     return count
#
#
# print(fn(800))
# print(14*8)
# print(len(filter(lambda n:n%7==0 ,range(1,input("请输入一个整数:")))))
# import tkinter
# class Application(tkinter.Frame):
#     def __init__(self, master=None):
#         tkinter.Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#     def createWidgets(self):
#         self.helloLabel = tkinter.Label(self, text='Hello, world!')
#         self.helloLabel.pack()
#         self.quitButton = tkinter.Button(self, text='Quit', command=self.quit)
#         self.quitButton.pack()
# app = Application()
# # 设置窗口标题:
# app.master.title('Hello World')
# # 主消息循环:
# app.mainloop()
# import tkinter
# import tkinter.messagebox
# class Application(tkinter.Frame):
#     def __init__(self,master=None):
#         super(Application,self).__init__(master)
#         self.pack()
#         self.createWidget()
#     def createWidget(self):
#         self.input=tkinter.Entry(self)
#         self.input.pack()
#         self.showMsg=tkinter.Button(self,text='showInfo',command=self.showInfo)
#         self.showMsg.pack()
#     def showInfo(self):
#         name=self.input.get() or 'world'
#         tkinter.messagebox.showinfo('Message', 'Hello, %s' % name)
#
#
# application = Application()
# application.master.title('Msg')
# application.mainloop()
import socket
import threading
import time

# socket_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket_socket.connect(('www.sina.com.cn', 80))
# # 发送数据:
# socket_socket.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n'.encode('utf-8'))
# buffer=[]
# while True:
#     recv = socket_socket.recv(1024)
#     if recv:
#         buffer.append(recv)
#     else:
#         break
# socket_socket.close()
# data = '.'.join(map(str,buffer))
# html=data.split('\r\n\r\n', 1)[0].encode(encoding='utf-8')
# # header,html=data.split('\r\n\r\n', 1)
# # print(header)
# with open('D:/test.html','wb') as f:
#     f.write(html)
def tcplink(sock,addr):
    print("Accept new connection from %s:%s..." % addr)
    sock.send(b'Welcome to python.org')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send(('Hello,%s!'%data).encode('utf-8'))
    sock.close()
    print("Connection from %s: %s closed." % addr)
# 服务端
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',9999))
s.listen(5)
print('waiting for server connect...')
while True:
    sock,addr = s.accept()
    thread = threading.Thread(target=tcplink, args=(sock, addr))
    thread.start()






