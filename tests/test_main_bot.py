""" Test main bot functions """
import pytest

# from Constants import API_KEY as KEY
from telegram.ext import Updater, Filters, MessageHandler

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher


def forwarder(update, context):
    msg = update.channel_post
    if msg:
        print(msg)


forwardHandler = MessageHandler(Filters.text & (~Filters.command), forwarder)
dispatcher.add_handler(forwardHandler)
updater.start_polling()
updater.idle()

#
# class TestExcelGen:
#
#     def setup_method(self, test_method):
#         # self.excel = ExcelGen('test_excel.xlsx')
#         # main.start()
#         pass
#
#     def teardown_method(self, test_method):
#         pass
#
#     def test_1(self):
#         main.start(update=update_sample, context=context_sample)
