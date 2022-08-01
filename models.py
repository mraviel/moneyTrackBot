from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Messages(db.Model):
    """ Messages model """

    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    is_expense = db.Column(db.Boolean, nullable=False, default=True)
    subject = db.Column(db.String(20), nullable=False)
    message_datetime = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)
