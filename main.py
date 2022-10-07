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
from DatabaseCommands import DatabaseCommands
from excel_generator import ExcelGen

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY

db_command = DatabaseCommands(db)
excel_gen = ExcelGen()

# Updater for telegram
updater = Updater(API_KEY, use_context=True)


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")

    author_id = update.message.from_user.id
    # Used for keep session sync
    with app.app_context():
        subjects = db_command.get_all_subjects(author_id=author_id)

        if not subjects:
            update.message.reply_text("I'v seen there are no subjects defined\n/add subjects for committing new rows")
        else:
            # subjects_title = list(filter(lambda subject: subject.subjects_title, subjects))
            subjects_title = ""
            for subject in subjects:
                subjects_title += "\n" + subject.subjects_title
            update.message.reply_text(f"Open subjects: {subjects_title}")


def helper(update: Update, context: CallbackContext):
    """ Helper func """
    text = str(P.help_message())
    update.message.reply_text(text)


def addSubject(update: Update, context: CallbackContext):
    """ Add subject """
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    # Get all the subjects
    subjects = context.args

    # Save all "subjects" to one subject
    main_subject = ""
    for subject in subjects:
        main_subject += subject + " "

    # Strip the last space
    main_subject = main_subject.strip()

    with app.app_context():
        # Check if subject already exists for the user
        current_subjects = db_command.get_all_subjects(author_id=author_id)
        for subject in current_subjects:
            if main_subject == subject.subjects_title:
                update.message.reply_text(f"This subject already exists")
                return

        db_command.add_subject(main_subject, author_id)
        update.message.reply_text(f"{main_subject} Saved")


def deleteSubject(update: Update, context: CallbackContext):
    """ Delete subject """
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    # Get all the subjects
    subjects = context.args

    # Save all "subjects" to one subject
    main_subject = ""
    for subject in subjects:
        main_subject += subject + " "

    # Strip the last space
    main_subject = main_subject.strip()

    # Get all subjects
    with app.app_context():

        is_deleted = db_command.delete_subject(main_subject, author_id)
        if is_deleted:
            update.message.reply_text(f"{main_subject} Deleted")
        else:
            update.message.reply_text(f"{main_subject} Not Found")


def deleteRow(update: Update, context: CallbackContext):
    """ Delete the last row in Messages table """
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    with app.app_context():
        last_message_obj = db_command.delete_last_row(author_id)

    update.message.reply_text(f"Delete Last Row ({last_message_obj.subject}: {last_message_obj.total})")


def exportToExcel(update: Update, context: CallbackContext):
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    current_month = int(datetime.now().strftime("%m"))
    current_year = int(datetime.now().strftime("%Y"))

    months_data = {}
    months_names = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)
        all_income = db_command.get_all_income(author_id=author_id)

        # loop throw all month pass for this year
        for i in range(1, current_month + 1):
            l_exp = []
            l_inc = []
            # Get the messages for the current month and year
            month_expenses = list(filter(lambda exp: exp.message_datetime.month == i
                                         and exp.message_datetime.year == current_year, all_expenses))

            month_income = list(filter(lambda inc: inc.message_datetime.month == i
                                       and inc.message_datetime.year == current_year, all_income))

            for expense in month_expenses:
                exp = [expense.subject, float(expense.total)]
                l_exp.append(exp)

            for income in month_income:
                inc = [income.subject, float(income.total)]
                l_inc.append(inc)

            months_data[months_names[i]] = [l_exp, l_inc]

        print(months_data)
        excel_gen.create_excel1(months_data)
        # print(months_data)

    update.message.reply_text("Export To Excel")
    # Process


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


def Sum(update: Update, context: CallbackContext):
    """ Calculate Income - all the expense's for current month"""

    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    current_month = int(datetime.now().strftime("%m"))
    current_year = int(datetime.now().strftime("%Y"))

    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)
        all_income = db_command.get_all_income(author_id=author_id)

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month
                                     and exp.message_datetime.year == current_year, all_expenses))
        month_income = list(filter(lambda exp: exp.message_datetime.month == current_month
                                   and exp.message_datetime.year == current_year, all_income))

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

        incomes = 0
        for income in month_income:
            incomes += income.total

        # Calculate the sum
        sum_for_now = expenses + incomes

    update.message.reply_text(str(sum_for_now))


def handle_message(update: Update, context: CallbackContext):
    """ Handle message """
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    # Recv text from user
    text = str(update.message.text).lower()

    # Process the message
    response = P.Expense(text)

    # If message is not valid
    if not response:
        update.message.reply_text(f"Not Valid")
        return

    data = {
        'message_id': update.message.message_id,
        'user_id': update.message.from_user.id,
        'message_datetime': update.message.date.ctime(),
        'is_expense': response['is_expense'],
        'subject': response['subject'],
        'total': response['total']
    }

    # Check if new message subject is in subjects list for user
    author_id = update.message.from_user.id
    with app.app_context():
        subjects = db_command.get_all_subjects(author_id=author_id)
        subjects_titles = []
        for subject in subjects:
            subjects_titles.append(subject.subjects_title)

    if data['subject'] in subjects_titles:
        # Save to DB
        with app.app_context():
            db_command.add_new_massage(data)

        # Send to user
        convertor = {True: '-', False: '+'}
        update.message.reply_text(f"Saved to DB ({data['subject']}: {convertor[data['is_expense']]}{data['total']})")

    else:
        update.message.reply_text(f"Subject: {data['subject']} not in your subjects\n/add him before using him")


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
    # updater.dispatcher.add_error_handler(error)

    # Start the session/ Every 5 seconds check for update
    updater.start_polling(5)

    updater.idle()
