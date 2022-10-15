from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import os
from Decorators import authorized_user


@authorized_user
def downloadExcel(update: Update, context: CallbackContext):
    """ Download Excel file from Excel List by index """
    author_id = update.message.from_user.id

    # Get Excel file name
    filename = ''
    args = context.args
    if args:
        filename = args[0]

    file_location = f'Excel/{author_id}/{filename}'
    if not os.path.exists(file_location):
        file_location = f'Excel/{author_id}/{filename}.xlsx'
        if not os.path.exists(file_location):
            update.message.reply_text(f"{filename}: not exists")
            return

    # Send the file
    update.message.reply_text(f"Download {filename} ...")
    chat_id = update.message.chat_id
    document = open(file_location, 'rb')
    context.bot.send_document(chat_id, document)

