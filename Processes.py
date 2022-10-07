import Constants as C


def check_if_me(author_id, update):
    # Only me can use this bot
    if str(author_id) != str(C.MY_ID):
        update.message.reply_text(f"You are not authorized for this bot")
        return False
    else:
        return True


# All the processes
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


def create_subjects_set(subjects_set, l: list):
    """ Create set object which contain all subjects that have been this year """

    # loop throw expenses
    for msg in l:
        subject = msg[0]
        if subject not in subjects_set:
            subjects_set.add(subject)


def group_data(subjects_set, data):

    """ Group togather data with same subject, the group activate as sum for amount """

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


def get_expense_and_income_subjects_set(months_data_group):
    """ Convert months_data dict to group months data """

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


def excel_file():
    pass


def help_message():
    return "I can help you keep track of your expenses and income" \
           "\nto help you find life balance." \
           "\nover time my functionality will grow." \
           "\n\nfor now here's a quick guide to help you use this bot:" \
           "\nTo Add new expense just put your subject in one side and the amount" \
           "\non the other side separate with ':' Example --> " \
           "\nFood: 40  //  אוכל: 50 שח " \
           "\nTo insert income just type '+' BEFORE the command" \
           "\n\nHere are some of the commands you can run:" \
           "\n/start --> Popup start message" \
           "\n/help --> Help section" \
           "\n/add --> Add new subject" \
           "\n/delsub --> Delete subject" \
           "\n/del --> remove row that added" \
           "\n/xl --> Export excel file with data (in dev)" \
           "\n/sum  --> All the expenses and income calculated for this month" \
           "\n/exp --> All the expenses for this month until now"



