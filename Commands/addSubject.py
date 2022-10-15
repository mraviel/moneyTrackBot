from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
import Processes as P


def addSubject(update: Update, context: CallbackContext):
    """ Add subject """
    author_id = update.message.from_user.id

    if not P.check_if_me(author_id, update):
        return

    # Get all the subjects
    subjects = context.args

    # Save all "subjects" to one subject
    main_subject = ""
    for subject in subjects:
        main_subject += subject + " "

    # Strip the last space
    main_subject = main_subject.strip()

    with app.app_context():
        # Check if subject already exists for the user
        current_subjects = db_command.get_all_subjects(author_id=author_id)
        for subject in current_subjects:
            if main_subject == subject.subjects_title:
                update.message.reply_text(f"This subject already exists")
                return

        db_command.add_subject(main_subject, author_id)
        update.message.reply_text(f"{main_subject} Saved")
