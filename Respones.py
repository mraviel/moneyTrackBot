import Constants as C


# All the responses
def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "sup"):
        return "Hi, who your doing"


def Expense(input_text):
    user_message = str(input_text).lower()
    if ':' in user_message:
        expense_type = user_message.split(':')[0]
        expense = user_message.split(':')[1]
        expense = C.strip_all(expense)

        return f"Type: {expense_type}, Expense: {expense}"



