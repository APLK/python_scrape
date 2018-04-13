# encoding:utf-8
'''
@author:lk

@time:2017/8/24 

@desc:

'''
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# encoding:utf-8
'''
@author:lk

@time:2017/8/24 

@desc:

'''
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(app.root_path, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)
db = SQLAlchemy(app)


class RoleBase(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='rolebase')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    db.create_all()
    admin_role = RoleBase(name='Admin')
    mod_role = RoleBase(name='Moderator')
    user_role = RoleBase(name='User')
    user_john = User(username='john', rolebase=admin_role)
    user_susan = User(username='susan', rolebase=user_role)
    user_david = User(username='david', rolebase=user_role)
    db.session.add(admin_role)
    db.session.add(mod_role)
    db.session.add(user_role)
    db.session.add(user_john)
    db.session.add(user_susan)
    db.session.add(user_david)
    admin_role.name = 'AdminRoot'
    # db.session.add_all([admin_role, mod_role, user_role,
    #     user_john, user_susan, user_david])
    db.session.commit()
    # print(User.query.all())
    # class Config(object):
    #     SQLALCHEMY_DATABASE_URI = os.path.join(app.root_path, 'sqlite.db')
    #     # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(app.root_path, 'sqlite.db')
    #     SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #     SQLALCHEMY_TRACK_MODIFICATIONS=True
    #
    # app.config.from_object(Config)
    # # app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:////' + os.path.join(app.root_path,'data.sqlite')
    # # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    #
    # db = SQLAlchemy(app)
    #
    # class Role(db.Model):
    #     __tablename__='role'
    #     id=db.Column(db.Integer,primary_key=True)
    #     name=db.Column(db.String(64),unique=True,index=True)
    #     user=db.relationship('User',backref='id')
    #     def __repr__(self):
    #         return 'Role %r'%self.name
    # class User(db.Model):
    #     __tablename__='user'
    #     id=db.Column(db.Integer,primary_key=True)
    #     username=db.Column(db.String(64),index=True,unique=True)
    #     role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    #     def __repr__(self):
    #         return 'User %r'%self.username
    #
    # if __name__=='__main__':
    #     app.run(debug=True)
    #     db.create_all()
