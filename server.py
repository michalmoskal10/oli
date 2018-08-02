from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_basicauth import BasicAuth

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(server)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String, unique=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Course %r>' % self.name


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String, unique=True)
    course_id = db.Column(db.String, db.ForeignKey('course.course_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Module %r>' % self.name

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, unique=True)
    course_id = db.Column(db.String, db.ForeignKey('course.course_id'), nullable=False)
    course_branch_id = db.Column(db.String)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.Integer, default=1)
    active_users = db.Column(db.Integer)
    active_users_enrolled = db.Column(db.Integer)
    users_enrolled = db.Column(db.Integer)

    def __repr__(self):
        return '<Session %r>' % self.session_id


class ModuleInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, db.ForeignKey('session.course_id'), nullable=False)
    module_id = db.Column(db.String, db.ForeignKey('module.course_id'), nullable=False)
    active_users = db.Column(db.Integer)


# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()

db.create_all()
print(Course.query.all())

with open('.pass') as f:
    VALID_USERNAME_PASSWORD_PAIRS = [x.strip().split(':') for x in f.readlines()]

username = VALID_USERNAME_PASSWORD_PAIRS[0][0]
password = VALID_USERNAME_PASSWORD_PAIRS[0][1]

server.config['BASIC_AUTH_USERNAME'] = username
server.config['BASIC_AUTH_PASSWORD'] = password
server.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(server)
