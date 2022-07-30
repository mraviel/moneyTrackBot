from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Messages(db.Model):
    """ Messages model """

    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.String(10), nullable=False)
    current_datetime = db.Column(db.Date, nullable=False, default=datetime.now())
