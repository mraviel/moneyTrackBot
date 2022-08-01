import threading
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
print([PSQL_KEY.strip('\n')])
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY.strip('\n')
db = SQLAlchemy(app)

updater = Updater(API_KEY, use_context=True)


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")


def handle_message(update: Update, context: CallbackContext):
    # Recv text from user
    text = str(update.message.text).lower()

    # Process the message
    response = P.Expense(text)
    message_id = update.message.message_id
    user_id = update.message.from_user.id
    message_datetime = update.message.date.ctime()
    subject = response['subject']
    total = response['total']

    Message = Messages(message_id=message_id, author_id=user_id, subject=subject, message_datetime=message_datetime, total=total)
    db.session.add(Message)
    db.session.commit()

    print(message_id, user_id, message_datetime, subject, total)

    # Send to user
    # update.message.reply_text(response)


def error(update: Update, context: CallbackContext):
    date = update.message.date.ctime()
    print(f"Update {update} caused error {context.error}")


# @app.route('/')
def main():

    # Handle Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Handle Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle errors
    #updater.dispatcher.add_error_handler(error)

    # Start the session
    updater.start_polling(5)

    updater.idle()


class FlaskThread(threading.Thread):
    def run(self):
        app.run()


class TelegramThread(threading.Thread):
    def run(self):
        main()


if __name__ == '__main__':

    flask_thread = FlaskThread()
    flask_thread.start()

    # telegram_thread = TelegramThread()

    main()


