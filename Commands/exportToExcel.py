from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from app import app
from app import db_command
import Processes as P
from datetime import datetime
from excel_generator import ExcelGen


def exportToExcel(update: Update, context: CallbackContext):
    author_id = update.message.from_user.id

    # Create Excel folder for this author
    P.create_excel_folder(author_id)

    # File name and file location
    excel_file_name = f'{datetime.now().strftime("%Y_%m_%d")}.xlsx'
    excel_file_location = f'Excel/{author_id}/{excel_file_name}'

    # Create the Excel file
    excel_gen = ExcelGen(excel_file_location)

    if not P.check_if_me(author_id, update):
        return

    # Get all messages for current user
    with app.app_context():
        all_expenses = db_command.get_all_expenses(author_id=author_id)
        all_income = db_command.get_all_income(author_id=author_id)
        months_data = P.create_months_data(all_income, all_expenses)

    # Fill the Excel file with data
    excel_gen.create_excel(months_data)

    # Send the file
    chat_id = update.message.chat_id
    document = open(excel_file_location, 'rb')
    context.bot.send_document(chat_id, document)

    update.message.reply_text("Export To Excel")

