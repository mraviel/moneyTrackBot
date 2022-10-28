# from main import db, create_app
from flask_sqlalchemy import SQLAlchemy

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



