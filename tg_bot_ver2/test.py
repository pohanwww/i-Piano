#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import configparser
import TG_handler_ver1
import pandas as pd
# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
TG_access_token = config['TELEGRAM']['TG_access_token']

import dropbox
from dropbox.files import WriteMode
import paho.mqtt.client as mqtt   #  pip install paho-mqtt

dbx = dropbox.Dropbox('jgH_djvkJasAAAAAAAAAFQslYkn9coLtRYvDeXQtXevRFR5WBAeHp42ZuLzUAly0')

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
TG_access_token = config['TELEGRAM']['TG_access_token']
imgur_client_id = config['IMGUR']['imgur_client_id']
imgur_client_secret = config['IMGUR']['imgur_client_secret']
imgur_album_id = config['IMGUR']['imgur_album_id']
imgur_access_token = config['IMGUR']['imgur_access_token']
imgur_refresh_token = config['IMGUR']['imgur_refresh_token']

TYPING_TITLE, SEARCH_SHEET, SCORE_RESULT = range(3)

temp_music_info = {
    'music_name': 'none',
    'music_sheet_url': 'none'
}

# Stages
FIRST, SECOND, SEARCH_SHEET, SONG_LIST = range(4)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    # logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("歌曲清單", callback_data=str(ONE)),
         InlineKeyboardButton("琴譜查詢", callback_data=str(TWO)),
         InlineKeyboardButton("分數查詢", callback_data=str(THREE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "請選擇功能",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update, context):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # Get Bot from CallbackContext
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("1", callback_data=str(ONE)),
         InlineKeyboardButton("2", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Start handler, Choose a route",
        reply_markup=reply_markup
    )
    return FIRST


def one(update, context):
    # """Show new choice of buttons"""
    # query = update.callback_query
    # bot = context.bot
    # keyboard = [
    #     [InlineKeyboardButton("3", callback_data=str(THREE)),
    #      InlineKeyboardButton("4", callback_data=str(FOUR))]
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    # bot.edit_message_text(
    #     chat_id=query.message.chat_id,
    #     message_id=query.message.message_id,
    #     text="First CallbackQueryHandler, Choose a route",
    #     reply_markup=reply_markup
    # )
    print('1')
    bot = context.bot
    #下載music_list檔案
    dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
    df = pd.read_csv('temp/music_list.csv', index_col=False)
    song_names = df['music_name'].values.tolist()
    print(song_names)
    text = 'Song list: \n'
    for index, item in enumerate(song_names):
        text += str(index+1)+ '. ' + item + '\n'
        print(text)
    print(update.message.from_user.id)
    bot.send_message(chat_id=update.message.from_user.id, text=text)
    return FIRST


def two(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("1", callback_data=str(ONE)),
         InlineKeyboardButton("3", callback_data=str(THREE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Second CallbackQueryHandler, Choose a route",
        reply_markup=reply_markup
    )
    return FIRST


def three(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
         InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Third CallbackQueryHandler. Do want to start over?",
        reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("2", callback_data=str(TWO)),
         InlineKeyboardButton("4", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Fourth CallbackQueryHandler, Choose a route",
        reply_markup=reply_markup
    )
    return FIRST


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TG_access_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(TG_handler_ver1.search_sheet_handler, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$')],
            SECOND: [CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                     CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')],
            SEARCH_SHEET: [MessageHandler(Filters.text, TG_handler_ver1.search_sheet)],
            SONG_LIST: [MessageHandler(Filters.text, TG_handler_ver1.song_list)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()