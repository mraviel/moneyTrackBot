from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command


def registerUser(update: Update, context: CallbackContext):
    """ Send request to join the bot """

    author_details = update.message.from_user

    with app.app_context():
        # Check if user already have access
        if db_command.get_user_exists(author_details.id):
            update.message.reply_text("You already have access for the bot")
            return

        if db_command.get_register_request_exists(author_details.id):
            update.message.reply_text("Your register already sent, It's may take a while before you'll get a response")
            return

        # Add register request to db
        author_details = author_details.to_dict()
        db_command.add_register_request(author_details)

        update.message.reply_text("Your register request has been sent, We'll notify you soon")

