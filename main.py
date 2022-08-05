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

        if not subjects:
            update.message.reply_text("I'v seen there are no subjects defined\n/add subjects for committing new rows")
        else:
            # subjects_title = list(filter(lambda subject: subject.subjects_title, subjects))
            subjects_title = ""
            for subject in subjects:
                subjects_title += "\n" + subject.subjects_title
            update.message.reply_text(f"Open subjects: {subjects_title}")


def helper(update: Update, context: CallbackContext):

    text = str(P.help_message())
    update.message.reply_text(text)


def addSubject(update: Update, context: CallbackContext):
    author_id = update.message.from_user.id

    # Get all the subjects
    subjects = context.args

    # Save all "subjects" to one subject
    main_subject = ""
    for subject in subjects:
        main_subject += subject + " "

    # Strip the last space
    main_subject = main_subject.strip()

    with app.app_context():
        new_subject = M.Subjects(author_id=author_id, subjects_title=main_subject)
        db.session.add(new_subject)
        db.session.commit()
        update.message.reply_text(f"{main_subject} Saved")


def deleteSubject(update: Update, context: CallbackContext):
    """ Delete subject """
    author_id = update.message.from_user.id

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
        subjects = M.Subjects.query.filter_by(author_id=author_id).all()

        # Search for subject and if exists delete it.
        for subject in subjects:

            if main_subject == subject.subjects_title:
                subject_obj = M.Subjects.query.filter_by(subjects_title=main_subject).first()  # Message to delete

                # Delete
                if subject_obj:
                    delete_subject = db.session.get(M.Subjects, subject_obj.id)
                    db.session.delete(delete_subject)
                    db.session.commit()
                    update.message.reply_text(f"{main_subject} Deleted")
                    return

        update.message.reply_text(f"{main_subject} Not Found")


def deleteRow(update: Update, context: CallbackContext):
    """ Delete the last row in Messages table """
    author_id = update.message.from_user.id

    # Get the last current user message
    with app.app_context():
        last_message_obj = M.Messages.query.filter_by(author_id=author_id).\
            order_by(M.Messages.message_id.desc()).first()

        print(last_message_obj)
        if last_message_obj:
            delete_last_message = db.session.get(M.Messages, last_message_obj.message_id)
            db.session.delete(delete_last_message)
            db.session.commit()

    update.message.reply_text(f"Delete Last Row ({last_message_obj.subject}: {last_message_obj.total})")


def exportToExcel(update: Update, context: CallbackContext):
    update.message.reply_text("Export To Excel")
    # Process


def Expenses(update: Update, context: CallbackContext):
    """ Get count of all my expenses this month """

    author_id = update.message.from_user.id
    current_month = int(datetime.now().strftime("%m"))

    # Get all messages for current user
    with app.app_context():
        all_expenses = M.Messages.query.filter_by(author_id=author_id, is_expense=True).all()

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month, all_expenses))

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

    update.message.reply_text(str(expenses))


def Sum(update: Update, context: CallbackContext):
    """ Calculate Income - all the expense's for current month"""

    author_id = update.message.from_user.id
    current_month = int(datetime.now().strftime("%m"))

    # Get all messages for current user
    with app.app_context():
        all_expenses = M.Messages.query.filter_by(author_id=author_id, is_expense=True).all()
        all_income = M.Messages.query.filter_by(author_id=author_id, is_expense=False).all()

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month, all_expenses))
        month_income = list(filter(lambda exp: exp.message_datetime.month == current_month, all_income))

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
        subjects = M.Subjects.query.filter_by(author_id=author_id).all()
        subjects_titles = []
        for subject in subjects:
            subjects_titles.append(subject.subjects_title)

    if data['subject'] in subjects_titles:
        # Save to DB
        with app.app_context():
            Message = M.Messages(message_id=data['message_id'], author_id=data['user_id'], subject=data['subject'],
                               message_datetime=data['message_datetime'], total=data['total'],
                                is_expense=data['is_expense'])

            db.session.add(Message)
            db.session.commit()

        # Send to user
        # update.message.reply_text(str(data))
        convertor = {True: '-', False: '+'}
        update.message.reply_text(f"Saved to DB ({data['subject']}: {convertor[data['is_expense']]}{data['total']})")

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

