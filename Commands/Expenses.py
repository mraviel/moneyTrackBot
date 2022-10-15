from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
from datetime import datetime
import Processes as P


def Expenses(update: Update, context: CallbackContext):
    """ Get count of all my expenses this month """

    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    current_month = int(datetime.now().strftime("%m"))
    current_year = int(datetime.now().strftime("%Y"))

    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month
                                     and exp.message_datetime.year == current_year, all_expenses))

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

    update.message.reply_text(str(expenses))

