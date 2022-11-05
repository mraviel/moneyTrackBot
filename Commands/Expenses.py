from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
from Decorators import authorized_user


@authorized_user
def Expenses(update: Update, context: CallbackContext):
    """ Get count of all my expenses this month """

    author_id = update.message.from_user.id

    # Get all messages for current user
    with app.app_context():

        # Get the messages for the current month
        month_expenses = db_command.get_this_month_expenses(author_id=author_id)

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

    update.message.reply_text(str(expenses))

