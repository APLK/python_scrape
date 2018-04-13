#encoding:utf-8
from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def go2Home():
   return render_template('home.html')
@app.route('/signin',methods=['GET'])
def signin():
    return render_template('form_submit.html')
@app.route('/signin1',methods=['POST'])
def sign_in():
    username_ = request.form['username']
    password_ = request.form['password']
    if username_=='张胖子' and password_=='123456':
        return render_template('success.html',username=username_)
    else:
        return render_template('form_submit.html',message="输入的帐号或密码有误",username=username_,password=password_)
if __name__=='__main__':
    app.run()
