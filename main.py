from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from Constants import API_KEY

# import commands
from Commands.start import start
from Commands.helper import helper
from Commands.addSubject import addSubject
from Commands.deleteSubject import deleteSubject
from Commands.deleteRow import deleteRow
from Commands.exportToExcel import exportToExcel
from Commands.Sum import Sum
from Commands.Expenses import Expenses
from Commands.handle_message import handle_message

# Updater for telegram
updater = Updater(API_KEY, use_context=True)


def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


def main():
    # Handle Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', helper))
    updater.dispatcher.add_handler(CommandHandler('add', addSubject, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('del', deleteRow))
    updater.dispatcher.add_handler(CommandHandler('delsub', deleteSubject, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('xl', exportToExcel))
    updater.dispatcher.add_handler(CommandHandler('sum', Sum))
    updater.dispatcher.add_handler(CommandHandler('exp', Expenses))

    # Handle Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle errors
    updater.dispatcher.add_error_handler(error)

    # Start the session/ Every 5 seconds check for update
    updater.start_polling(5)

    updater.idle()
