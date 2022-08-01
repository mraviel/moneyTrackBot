from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Constants import API_KEY, PSQL_KEY
import Processes as P
from models import Messages
from datetime import datetime

# config app
app = Flask(__name__)
app.secret_key = 'replace later'
socketio = SocketIO(app)

# Config db
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY
db = SQLAlchemy(app)

# Updater for telegram
updater = Updater(API_KEY, use_context=True)


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")


def helper(update: Update, context: CallbackContext):
    update.message.reply_text("Helper")


def addSubject(update: Update, context: CallbackContext):
    update.message.reply_text("addSubject")


def showSubjects(update: Update, context: CallbackContext):
    update.message.reply_text("All My Subjects")


def deleteRow(update: Update, context: CallbackContext):
    update.message.reply_text("Delete Last Row")


def exportToExcel(update: Update, context: CallbackContext):
    update.message.reply_text("Export To Excel")


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

    Message = Messages(message_id=data['message_id'], author_id=data['user_id'], subject=data['subject'],
                       message_datetime=data['message_datetime'], total=data['total'])

    db.session.add(Message)
    db.session.commit()

    print(data)

    # Send to user
    update.message.reply_text(str(data))
    update.message.reply_text("Saved to DB")


def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


# @app.route('/')
def main():

    # Handle Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', helper))
    updater.dispatcher.add_handler(CommandHandler('add', addSubject))
    updater.dispatcher.add_handler(CommandHandler('del', deleteRow))
    updater.dispatcher.add_handler(CommandHandler('all', showSubjects))
    updater.dispatcher.add_handler(CommandHandler('xl', exportToExcel))

    # Handle Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle errors
    updater.dispatcher.add_error_handler(error)

    # Start the session/ Every 5 seconds check for update
    updater.start_polling(5)

    updater.idle()

