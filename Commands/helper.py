from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
import Processes as P


def helper(update: Update, context: CallbackContext):
    """ Helper func """
    text = str(P.help_message())
    update.message.reply_text(text)
