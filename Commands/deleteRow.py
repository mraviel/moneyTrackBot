from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
from Decorators import authorized_user


@authorized_user
def deleteRow(update: Update, context: CallbackContext):
    """ Delete the last row in Messages table """
    author_id = update.message.from_user.id

    with app.app_context():
        last_message_obj = db_command.delete_last_row(author_id)

    update.message.reply_text(f"Delete Last Row ({last_message_obj.subject}: {last_message_obj.total})")

