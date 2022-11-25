import os
from datetime import datetime
import Constants as C


def Expense(input_text):
    user_message = str(input_text).lower()
    if ':' in user_message:
        type_of = user_message.split(':')[0]
        amount = user_message.split(':')[1]
        amount = C.strip_all(amount)

        # Only numbers pass
        try:
            float(amount)
        except ValueError:
            return None

        # Check if income or expense and send
        if '+' == user_message[0]:
            type_of = type_of[1:]
            return {'subject': type_of, 'total': float(amount), 'is_expense': False}
        else:
            return {'subject': type_of, 'total': float(amount), 'is_expense': True}

    else:
        return None


def create_months_data(all_income, all_expenses):
    """ Args: all_income: (list) all the income messages from db
    Args: all_expenses: (list) all the expenses messages from db
    Return months_data {dict} months as keys, with income and expenses for each month as values """

    current_month = int(datetime.now().strftime("%m"))
    current_year = int(datetime.now().strftime("%Y"))

    months_data = {}
    months_names = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

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

    return months_data


def create_subjects_set(subjects_set: set, data: list):
    """ Create set object which contain all subjects that have been this year
        Args: subjects_set: (set) of all unique subjects,
        data: (list) store the amounts of subjects """

    # loop throw subjects
    for msg in data:
        subject = msg[0]
        if subject not in subjects_set:
            subjects_set.add(subject)


def group_data(subjects_set: set, data: list):
    """ Group togather data with same subject, the group activate as sum for amount.
        Args: subjects_set: (set) of all unique subjects
              data: (list) [[income], [expenses]]
        Return list with group subjects and the sum of the amount of the subject """

    group_sub_total = []
    for sub_set in subjects_set:
        # Filter subjects togather by subject and current month
        group = list(filter(lambda x: sub_set in x, data))

        # Loop throw all group and added them to new dict
        total_for_subject = 0
        for msg in group:
            amount = msg[1]
            total_for_subject += amount

        group_sub_total.append([sub_set, total_for_subject])

    return group_sub_total


def convert_months_data_to_group(months_data):
    """ Convert months_data dict to group months data """

    subjects_set_expenses = set()
    subjects_set_income = set()
    months_data_group = {}

    # Loop over all months and gather all used subjects
    for month, data in months_data.items():  # data = [[income], [expenses]]

        expenses = data[0]
        income = data[1]

        # loop throw expenses
        create_subjects_set(subjects_set_expenses, expenses)

        # loop throw income
        create_subjects_set(subjects_set_income, income)

        group_expenses = group_data(subjects_set_expenses, expenses)
        group_income = group_data(subjects_set_income, income)

        # Add to dict
        months_data_group[month] = [group_expenses, group_income]

    return months_data_group


def get_expense_and_income_subjects_set(months_data_group: dict):
    """ Args: months_data_group: (dict)
        Return (dict) with total subjects of income/expenses keys(income_set, expense_set) """

    subjects_set_expenses = set()
    subjects_set_income = set()

    # Loop over all months and gather all used subjects
    for month, data in months_data_group.items():  # data = [[income], [expenses]]

        expenses = data[0]
        incomes = data[1]

        # loop throw expenses
        create_subjects_set(subjects_set_expenses, expenses)

        # loop throw income
        create_subjects_set(subjects_set_income, incomes)

    return {'expense_set': list(subjects_set_expenses), 'income_set': list(subjects_set_income)}


def create_excel_folder(author_id):
    """ Create Excel folder which store all files for users """
    if not os.path.isdir('Excel'):
        os.mkdir(f'Excel')

    if not os.path.isdir(f'Excel/{author_id}'):
        os.mkdir(f'Excel/{author_id}')


def help_message():
    return "This bot design to help you keep track of your money" \
           "\nto help you find life balance." \
           "\n\nHere's a quick guide to help you start:" \
           "\nTo Add new expense just put your subject in one side and the amount" \
           "\non the other side separate with ':'" \
           "\nExample --> Food: 40  //  אוכל: 50 שח " \
           "\nTo insert income just type '+' before the subject" \
           "\n\nAvailable functions:" \
           "\n/register : Send request to register" \
           "\n/start : Popup start message" \
           "\n/help : Help section" \
           "\n/add : Add new subject" \
           "\n/delsub : Delete subject" \
           "\n/del : Remove last added row" \
           "\n/xl : Export excel file" \
           "\n/sum : Total income - expenses" \
           "\n/exp : Total expenses for the month" \
           "\n/xlist : List of xl files stores for me" \
           "\n/xlsave : Download an old Excel file"
