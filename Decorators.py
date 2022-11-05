import functools
from app import app, db_command


def authorized_user(func):
    """ Function that behave as a decorator, Check if user is authorized if not: Return None """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        update = args[0]
        author_id = update.message.from_user.id
        with app.app_context():
            db_user = db_command.get_user_exists(author_id)
            if not db_user:
                update.message.reply_text(f"You are not authorized for this bot")
                return
        func(*args, **kwargs)
    return wrapper

