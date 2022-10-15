from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import os
from Decorators import authorized_user


@authorized_user
def excelList(update: Update, context: CallbackContext):
    """ Return the current Excel files that have been saved for the user """
    author_id = update.message.from_user.id
    current_excel_files = os.listdir(f'Excel/{author_id}/')

    update.message.reply_text(f"List of files to download, use command /xlsave with file name")
    update.message.reply_text(f"{current_excel_files}")

