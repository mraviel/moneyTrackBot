from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command


# Message when bot activate
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello And Wellcome to my bot")

    author_id = update.message.from_user.id
    # Used for keep session sync
    with app.app_context():
        subjects = db_command.get_all_subjects(author_id=author_id)

        if not subjects:
            update.message.reply_text("I'v seen there are no subjects defined\n/add subjects for committing new rows")
        else:
            # subjects_title = list(filter(lambda subject: subject.subjects_title, subjects))
            subjects_title = ""
            for subject in subjects:
                subjects_title += "\n" + subject.subjects_title
            update.message.reply_text(f"Open subjects: {subjects_title}")
