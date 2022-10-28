from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
import requests


def registerUser(update: Update, context: CallbackContext):
    """ Send request to join the bot """

    author_details = update.message.from_user

    with app.app_context():
        # Check if user already have access
        if db_command.get_user_exists(author_details.id):
            update.message.reply_text("You already have access for the bot")
            return

        # Send POST request for the api
        url = "http://127.0.0.1:5000/register_request"
        author_details = author_details.to_dict()
        response = requests.post(url, json=author_details)
        print(response.text)

        update.message.reply_text("Your register request has been sent, We'll notify you soon")


        # db_command.add_user(author_details)

