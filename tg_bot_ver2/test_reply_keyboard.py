import sys
import time
import configparser
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

config = configparser.ConfigParser()
config.read('config.ini')
TG_access_token = config['TELEGRAM']['TG_access_token']

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    if content_type == 'text':
        if msg['text'] == '/key':
            bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ]
                            ))


# TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TG_access_token)
print(bot)
print('Listening ...')
bot.message_loop({'chat': on_chat_message}, run_forever=True)