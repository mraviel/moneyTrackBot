import Constants as C


# All the processes
def Expense(input_text):
    user_message = str(input_text).lower()
    if ':' in user_message:
        type_of = user_message.split(':')[0]
        amount = user_message.split(':')[1]
        amount = C.strip_all(amount)

        return {'subject': type_of, 'total': amount}

        # return f"Type: {expense_type}, Expense: {expense}"


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
           "\n/del --> remove row that added" \
           "\n/xl --> Export excel file with data" \
           "\n/sum  --> All the expenses for this month until now"



