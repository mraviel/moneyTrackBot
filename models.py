from main import db, create_app


class Subjects(db.Model):
    """ Subjects model """

    __tablename__ = "subjects"
    author_id = db.Column(db.Integer, primary_key=True)
    subjects_title = db.Column(db.String(20), nullable=False)


class Messages(db.Model):
    """ Messages model """

    __tablename__ = "messages"
    # id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('subjects.author_id'), nullable=False)
    is_expense = db.Column(db.Boolean, nullable=False, default=True)
    subject = db.Column(db.String(20), nullable=False)
    message_datetime = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)



