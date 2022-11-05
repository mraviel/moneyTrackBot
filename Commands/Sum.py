from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
from Decorators import authorized_user


@authorized_user
def Sum(update: Update, context: CallbackContext):
    """ Calculate Income - all the expense's for current month"""

    author_id = update.message.from_user.id

    # Get all messages for current user
    with app.app_context():

        # Get the messages for the current month
        month_expenses = db_command.get_this_month_expenses(author_id=author_id)
        month_income = db_command.get_this_month_income(author_id=author_id)

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

        incomes = 0
        for income in month_income:
            incomes += income.total

        # Calculate the sum
        sum_for_now = expenses + incomes

    update.message.reply_text(str(sum_for_now))

