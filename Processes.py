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



