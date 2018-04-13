#encoding:utf-8
# import socket
# socket_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# socket_socket.connect(('127.0.0.1',9999))
# print(socket_socket.recv(1024))
# for data in ['Michael', 'Tracy', 'Sarah']:
#     # 发送数据:
#     socket_socket.send(data.encode('utf-8'))
#     print(socket_socket.recv(1024))
# # socket_socket.send(lambda n:n.encode('utf-8') for x in ['Michael', 'Tracy', 'Sarah'])
#
# socket_socket.send('exit'.encode(encoding='utf-8'))
# socket_socket.close()
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, str) else addr))

msg = MIMEText('life is short,i use wanshe', 'utf-8')
msg['From'] = "hwlk_90 <hwlk_90@163.com>"
msg['To'] = "zhangning <1586863639@qq.com>"
msg['Subject'] = 'kangmei.com'

login_addr = 'hwlk_90@163.com'
login_pwd = 'sq163lk'
server = 'smtp.163.com'
send_addr1 = '1586863639@qq.com'
# send_addr2 = '1399424199@qq.com'

# msg['From'] = _format_addr(u'我 <%s>' % login_addr)
# msg['To'] = _format_addr(u'tlby <%s>' % send_addr)
# msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

# login_addr = input('请输入登录的邮箱地址:')
# login_pwd = input('请输入登录的邮箱密码:')
# server = input('请输入服务端口名称:')
# send_addr = input('请输入发送的邮箱地址:')
smtplib_smtp = smtplib.SMTP(server, 25)
smtplib_smtp.set_debuglevel(1)
smtplib_smtp.login(login_addr,login_pwd)
smtplib_smtp.sendmail(login_addr,[send_addr1],msg.as_string())
smtplib_smtp.quit()

