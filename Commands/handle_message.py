from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
import Processes as P
from datetime import datetime
from Decorators import authorized_user


@authorized_user
def handle_message(update: Update, context: CallbackContext):
    """ Handle message """
    author_id = update.message.from_user.id

    # Recv text from user
    text = str(update.message.text).lower()

    # Process the message
    response = P.Expense(text)

    # If message is not valid
    if not response:
        update.message.reply_text(f"Not Valid")
        return

    data = {
        'message_id': update.message.message_id,
        'user_id': update.message.from_user.id,
        'message_datetime': datetime.now().ctime(),
        'is_expense': response['is_expense'],
        'subject': response['subject'],
        'total': response['total']
    }

    # Check if new message subject is in subjects list for user
    author_id = update.message.from_user.id
    with app.app_context():
        subjects = db_command.get_all_subjects(author_id=author_id)
        subjects_titles = []
        for subject in subjects:
            subjects_titles.append(subject.subjects_title)

    if data['subject'] in subjects_titles:
        # Save to DB
        with app.app_context():
            db_command.add_new_massage(data)

        # Send to user
        convertor = {True: '-', False: '+'}
        update.message.reply_text(f"({data['subject']}: {convertor[data['is_expense']]}{data['total']}) Saved")

    else:
        update.message.reply_text(f"Subject: {data['subject']} not in your subjects\nfirst /add the subject")
