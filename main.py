from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Constants import API_KEY, PSQL_KEY
import Processes as P
from datetime import datetime
import threading
import models as M

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY

# Updater for telegram
updater = Updater(API_KEY, use_context=True)


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")

    author_id = update.message.from_user.id
    # Used for keep session sync
    with app.app_context():
        subjects = M.Subjects.query.filter_by(author_id=author_id).all()
        print(subjects)

        if not subjects:
            update.message.reply_text("I'v seen there are no subjects defined\n/add subjects for committing new rows")
        else:
            update.message.reply_text(f"Open subjects: {str(subjects)}")


def helper(update: Update, context: CallbackContext):

    text = str(P.help_message())
    update.message.reply_text(text)


def addSubject(update: Update, context: CallbackContext):
    author_id = update.message.from_user.id
    subjects = context.args
    print(subjects)
    for subject in subjects:
        with app.app_context():
            print(subject)
            new_subject = M.Subjects(author_id=author_id, subjects_title=subject)
            db.session.add(new_subject)
            db.session.commit()
            update.message.reply_text(f"{subject} Saved")


def showSubjects(update: Update, context: CallbackContext):
    update.message.reply_text("All My Subjects")
    # sql


def deleteRow(update: Update, context: CallbackContext):
    """ Delete the last row in Messages table """
    author_id = update.message.from_user.id
    with app.app_context():
        last_message_obj = M.Messages.query.filter_by(author_id=author_id).last()
        if last_message_obj:
            delete_last_message = db.session.get(M.Messages, last_message_obj.message_id)
            db.session.delete(delete_last_message)
            db.session.commit()

    update.message.reply_text("Delete Last Row")
    # sql


def exportToExcel(update: Update, context: CallbackContext):
    update.message.reply_text("Export To Excel")
    # Process


def handle_message(update: Update, context: CallbackContext):
    # Recv text from user
    text = str(update.message.text).lower()

    # Process the message
    response = P.Expense(text)
    data = {
        'message_id': update.message.message_id,
        'user_id': update.message.from_user.id,
        'message_datetime': update.message.date.ctime(),
        'subject': response['subject'],
        'total': response['total']
    }

    # Check if new message subject is in subjects list for user
    author_id = update.message.from_user.id
    with app.app_context():
        subjects = M.Subjects.query.filter_by(author_id=author_id).all()
        subjects_titles = []
        for subject in subjects:
            subjects_titles.append(subject.subjects_title)

    if data['subject'] in subjects_titles:

        # Save to DB
        with app.app_context():
            Message = M.Messages(message_id=data['message_id'], author_id=data['user_id'], subject=data['subject'],
                               message_datetime=data['message_datetime'], total=data['total'])

            db.session.add(Message)
            db.session.commit()

        print(data)

        # Send to user
        update.message.reply_text(str(data))
        update.message.reply_text("Saved to DB")

    else:
        update.message.reply_text(f"Subject: {data['subject']} not in your subjects\n/add him before using him")


def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


# @app.route('/')
def main():

    # Handle Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', helper))
    updater.dispatcher.add_handler(CommandHandler('add', addSubject, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('del', deleteRow))
    updater.dispatcher.add_handler(CommandHandler('all', showSubjects))
    updater.dispatcher.add_handler(CommandHandler('xl', exportToExcel))

    # Handle Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle errors
    # updater.dispatcher.add_error_handler(error)

    # Start the session/ Every 5 seconds check for update
    updater.start_polling(5)

    updater.idle()

