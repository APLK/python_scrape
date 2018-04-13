# encoding:utf-8
from flask import Flask
from flask import request

flak = Flask(__name__)


@flak.route('/', methods=['GET', 'POST'])
def go2Main():
    return '<h1>Welcome to Home!</h1>'


@flak.route('/signin',methods=['GET'])
def signin_form():
    return '''<form action='/signin' method='post'>
    <p>请输入用户名称:<input name='username'></p>
    <p>请输入密码:<input name='password' type='password'></p>
    <p><button type='submit'>提交</button></p>
</form>'''
@flak.route('/signin', methods=['POST'])
def signin():
# 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'
if __name__=='__main__':
    flak.run()

