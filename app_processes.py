from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Constants import API_KEY, PSQL_KEY
from DatabaseCommands import DatabaseCommands



db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY

db_command = DatabaseCommands(db)


def start_process(update, author_id):
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


def addSubject_process(update, author_id, main_subject):

    with app.app_context():
        # Check if subject already exists for the user
        current_subjects = db_command.get_all_subjects(author_id=author_id)
        for subject in current_subjects:
            if main_subject == subject.subjects_title:
                update.message.reply_text(f"This subject already exists")
                return

        db_command.add_subject(main_subject, author_id)
        update.message.reply_text(f"{main_subject} Saved")


def deleteSubject_process(update, author_id, main_subject):
    # Get all subjects
    with app.app_context():

        is_deleted = db_command.delete_subject(main_subject, author_id)
        if is_deleted:
            update.message.reply_text(f"{main_subject} Deleted")
        else:
            update.message.reply_text(f"{main_subject} Not Found")


def deleteRow_process(update, author_id):

    with app.app_context():
        return db_command.delete_last_row(author_id)


def exportToExcel_process(update, author_id, current_month):
    # Get all messages for current user
    l_exp = []
    l_inc = []

    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)
        all_income = db_command.get_all_income(author_id=author_id)

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month, all_expenses))
        month_income = list(filter(lambda exp: exp.message_datetime.month == current_month, all_income))

        for expense in month_expenses:
            exp = [expense.subject, expense.total]
            l_exp.append(exp)

        for income in month_income:
            inc = [income.subject, income.total]
            l_inc.append(inc)

        # Call function that takes two types of lists


def Expenses_process(update, author_id, current_month):
    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)

        # Get the messages for the current month
        month_expenses = list(filter(lambda exp: exp.message_datetime.month == current_month, all_expenses))

        expenses = 0
        for expense in month_expenses:
            expenses -= expense.total

        return expenses


def Sum_process(update, author_id, current_month):

    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)
        all_income = db_command.get_all_income(author_id=author_id)

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

        return sum_for_now


def handel_message_process(update, data):
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

