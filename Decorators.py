import Constants as C
import functools


def authorized_user(func):
    """ Function that behave as a decorator, Check if user is authorized if not: Return None """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        update = args[0]
        lines = open('authorized_users.txt', 'r').readlines()
        lines = list(map(lambda line: line.strip(), lines))  # remove \n
        if str(C.MY_ID) not in lines:
            update.message.reply_text(f"You are not authorized for this bot")
            return
        func(*args, **kwargs)
    return wrapper
