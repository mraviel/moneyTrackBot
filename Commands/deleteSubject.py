from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
from Decorators import authorized_user


@authorized_user
def deleteSubject(update: Update, context: CallbackContext):
    """ Delete subject """
    author_id = update.message.from_user.id

    # Get all the subjects
    subjects = context.args

    # Save all "subjects" to one subject
    main_subject = ""
    for subject in subjects:
        main_subject += subject + " "

    # Strip the last space
    main_subject = main_subject.strip()

    # Get all subjects
    with app.app_context():

        is_deleted = db_command.delete_subject(main_subject, author_id)
        if is_deleted:
            update.message.reply_text(f"{main_subject} Deleted")
        else:
            update.message.reply_text(f"{main_subject} Not Found")

