# from main import db, create_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from Constants import Admin_Username, Admin_Password

db = SQLAlchemy()


class Subjects(db.Model):
    """ Subjects model """

    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, unique=True, nullable=False)
    subjects_title = db.Column(db.String(20), nullable=False)


class Messages(db.Model):
    """ Messages model """

    __tablename__ = "messages"
    # id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    is_expense = db.Column(db.Boolean, nullable=False, default=True)
    message_datetime = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Numeric, nullable=False)


class Users(db.Model):
    """ Users model """

    __tablename__ = "users"
    #id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)

    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    is_bot = db.Column(db.Boolean, nullable=False)
    language_code = db.Column(db.String, nullable=False)


class AdminUser(UserMixin):
    # proxy for a database of users
    user_database = {"admin": (Admin_Username, Admin_Password)}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    @classmethod
    def get(cls, id):
        data = cls.user_database.get(id)
        return AdminUser(data[0], data[1])
