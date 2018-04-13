# encoding:utf-8

import hashlib

from collections import defaultdict

import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_uploads import IMAGES, TEXT, UploadSet, configure_uploads
from werkzeug.utils import secure_filename, escape

__author__ = 'APLK'
'''
  通常，登陆某个网站或者 APP，需要使用用户名和密码。密码是如何加密后存储起来的呢？请使用 Python 对密码加密。
'''

app = Flask(__name__)
basepath = os.path.dirname(__file__)  # 当前文件所在路径
app.config['UPLOADED_TEXT_DEST'] = os.path.join(os.path.dirname(__file__),'static/uploads')
app.config['UPLOADED_TEXT_ALLOW'] = TEXT
photos = UploadSet('TEXT')
configure_uploads(app, photos)

db = {}
# db = defaultdict(lambda: 'N/A')                     #去掉登录可能产生的KeyError
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def get_md5(password):
    a = hashlib.md5()
    a.update(password . encode('utf-8'))
    return (a.hexdigest())

def saveAccount(username, password):
    # db.clear()
    db[username] = get_md5(password + username + 'the-Salt')
    # print(list(db.keys())[0])

def getAccount(username, password):
    b = get_md5(password + username + 'the-Salt' )
    if username in db.keys() and b==db[username]:
        return True
    else:
        return False
@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')
@app.route('/home/<username>',methods=['GET'])
def goHome(username):
    print(db)
    if 'phone' in session and len(db)!=0 and username in db.keys():
        print('Logged in as %s' % escape(session['phone']))
        print('Logged in as %s' % session['phone'])
        return render_template('home.html',username=username)
    return redirect('/login', code=302)
@app.route('/index',methods=['POST'])
def loginOut():
    session.pop('username', None)
    return redirect('/login', code=302)
@app.route('/register_submit',methods=['POST'])
def register_submit():
    phone_ = request.form['phone']
    nickname_ = request.form['nickname']
    setpassword_ = request.form['setpassword']
    # print(phone_)
    if phone_ =='':
        message='手机号不能为空'
        return render_template('register.html',message=message)
    if nickname_  =='':
        message='昵称不能为空'
        return render_template('register.html',message=message)
    if setpassword_  =='':
        message='密码不能为空'
        return render_template('register.html',message=message)
    saveAccount(phone_,setpassword_)
    session['phone'] = request.form['phone']
    # return redirect('/home', code=302)
    return redirect(url_for('goHome', username=phone_))
@app.route('/login_submit',methods=['POST'])
def login_submit():
    phone_ = request.form['phone']
    password_ = request.form['password']
    if phone_  =='':
        message='手机号不能为空'
        return render_template('login.html',message=message)
    if password_  =='':
        message='密码不能为空'
        return render_template('login.html',message=message)
    b = getAccount(phone_, password_)
    if b:
        session['phone'] = request.form['phone']
        # return redirect('/home', code=302)
        return redirect(url_for('goHome', username=phone_))
    else:
        message='用户名或密码不正确,请重新输入'
        return render_template('login.html',message=message)
@app.route('/')
def index(): pass

@app.route('/login1')
def login1(): pass

@app.route('/user/<username>')
def profile(username): pass

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # if request.method == 'POST':
    #     f = request.files['file']
    #     print(f)
    #     basepath = os.path.dirname(__file__)  # 当前文件所在路径
    #     print(basepath)
    #     # upload_path = os.path.join(basepath, 'static/uploads',f)  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    #     upload_path = os.path.join(basepath, 'static/uploads',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    #     print(upload_path)
    #     stream = f.stream.read().decode('utf-8')
    #     stream.save(upload_path)
    #     # return redirect('/upload', code=302)
    #     return redirect(url_for('upload'))
    # return render_template('upload.html')
    if request.method == 'POST' and 'file' in request.files:
        photos.save(request.files['file'])
        return redirect(url_for('upload'))
    return render_template('upload.html')
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',error='404'), 404

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login1'))
#     print(url_for('login1', next='/'))
#     print(url_for('profile', username='John Doe'))
if __name__=='__main__':
    app.debug = True
    app.run()