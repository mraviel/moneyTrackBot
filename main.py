from flask import Flask
from flask_socketio import SocketIO
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Constants import API_KEY
import Respones as R
from datetime import datetime

# config app
app = Flask(__name__)
app.secret_key = 'replace later'
socketio = SocketIO(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = KEY

updater = Updater(API_KEY, use_context=True)


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")


def handle_message(update: Update, context: CallbackContext):
    # Recv text from user
    text = str(update.message.text).lower()

    # Process the message
    response = R.Expense(text)

    # Send to user
    update.message.reply_text(response)


def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


@app.route('/')
def main():

    # Handle Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Handle Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle errors
    updater.dispatcher.add_error_handler(error)

    # Start the session
    updater.start_polling(5)

    updater.idle()


if __name__ == '__main__':

    # app.run(debug=False)
    socketio.run(app, debug=False)



