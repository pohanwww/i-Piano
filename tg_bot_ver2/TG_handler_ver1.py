from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from imgurpython import ImgurClient
import pandas as pd
import configparser
import random
import time
import cv2
import os
import img_process
import sys
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

# *********************************************************************
# MQTT Config

MQTT_SERVER = "broker.hivemq.com"  
MQTT_PORT = 1883  
MQTT_ALIVE = 60  

MQTT_po_song  = "po/song/"
MQTT_po_user  = "po/song/user/"
MQTT_po_pic   = "po/pic_url/"
MQTT_po       = "po/"
MQTT_po_score = "/score/"
# *********************************************************************


mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)

#圖片input處理>>
def image_handler(bot, update):
    start_time = time.time()
    update.message.reply_text('下載中...')
    file = bot.getFile(update.message.document.file_id)
    file.download('temp/src_image.jpg')
    print("download finish", time.time()-start_time)

    img_process.image_process_1()

    try:
        client = ImgurClient(imgur_client_id, imgur_client_secret, imgur_access_token, imgur_refresh_token)
        config = {
            'album': imgur_album_id,
            'name': 'TG_image',
            'title': 'TG_image',
            'description': 'TG_image'
        }
        uploaded_img = client.upload_from_path("temp/dstImg.png", config=config, anon=False)
        # print(uploaded_img)
        url = uploaded_img['link']
        temp_music_info['music_sheet_url'] = [url]
        
    except:
        print('上傳失敗')

    bot.send_photo(chat_id=update.message.from_user.id, photo=uploaded_img['link'])
    
    update.message.reply_text('這首曲子叫甚麼名字呢?')
    print("上傳完畢", time.time()-start_time)
    return TYPING_TITLE

def handle_title(bot, update):
    text = update.message.text
    temp_music_info['music_name'] = [text]
    #下載music_list檔案
    dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
    ########
    # df = pd.DataFrame.from_dict(temp_music_info)
    # df.to_csv('temp/music_list.csv', encoding="utf_8_sig", index=False)
    ##############
    df = pd.read_csv('temp/music_list.csv', index_col=False)
    df_temp = pd.DataFrame.from_dict(temp_music_info)
    df = df.append(df_temp)
    df.to_csv('temp/music_list.csv', encoding="utf_8_sig", index=False)

    #上傳music_list檔案
    with open('temp/music_list.csv', 'rb') as f:
        dbx.files_upload(f.read(), '/i_Piano/music_list.csv', mode=WriteMode('overwrite'))

    #上傳 Node-Red
    song_names = df['music_name'].values.tolist()
    pic_urls = df['music_sheet_url'].values.tolist()

    for i, song_name in enumerate(song_names):
        mqtt_client.publish( MQTT_po_song + str(i+1) , song_name)
        mqtt_client.publish( MQTT_po_pic + str(i+1) , "http://i.imgur.com/wSvUkHG.png")
        # print(pic_urls[i])

    update.message.reply_text('處理圖片中...')

    img_process.image_process_2()
    #上傳midi檔案
    with open('temp/output.mid', 'rb') as f:
        dbx.files_upload(f.read(), '/i_Piano/'+text+'.mid', mode=WriteMode('overwrite'))
    #上傳object檔案
    with open('temp/output.txt', 'rb') as f:
        dbx.files_upload(f.read(), '/i_Piano/'+text+'.txt', mode=WriteMode('overwrite'))

    #傳midi給使用者
    bot.send_document(chat_id=update.message.from_user.id, document=open('temp/output.mid', 'rb'))

    update.message.reply_text('已為您完整儲存檔案')

    return ConversationHandler.END
#圖片input處理<<

#/search功能>>
def search_sheet_handler(bot, update):
    update.message.reply_text('請問您要找的曲名?')
    return SEARCH_SHEET

def search_sheet(bot, update):
    text = update.message.text
    #下載music_list檔案
    dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
    print('1')
    df = pd.read_csv('temp/music_list.csv', index_col=False, encoding="utf_8_sig")
    print('2')
    url = df.loc[df['music_name'] == text]['music_sheet_url'].values[0]
    #傳圖片給使用者
    bot.send_photo(chat_id=update.message.from_user.id, photo=url)

    #下載midi檔案
    dbx.files_download_to_file('temp/' +text+ '.mid', '/i_Piano/' +text+ '.mid')
    #傳midi給使用者
    bot.send_document(chat_id=update.message.from_user.id, document=open('temp/' +text+ '.mid', 'rb'))

    return ConversationHandler.END
#/search功能<<

#搜尋樂曲清單
def song_list(bot, update):
    #下載music_list檔案
    dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
    df = pd.read_csv('temp/music_list.csv', index_col=False)
    song_names = df['music_name'].values.tolist()
    # print(song_names)
    text = 'Song list: \n'
    for index, item in enumerate(song_names):
        text += str(index+1)+ '. ' + item + '\n'
        
    bot.send_message(chat_id=update.message.from_user.id, text=text)

#搜尋分數排名
def score_handler(bot, update):
    update.message.reply_text('請問您要找哪一首的分數?')
    return SCORE_RESULT

def score_result(bot, update):
    text = update.message.text
    dbx.files_download_to_file('temp/song_score.csv', '/i_Piano/' +text+ '.csv')
    
    df = pd.read_csv('temp/song_score.csv', index_col=False)
    user_list = df.values.tolist()
    print(user_list)
    text = 'Song score: \n'
    for index, item in enumerate(user_list):
        text += str(index+1)+ '. ' + item[0] + ': ' + str(item[1]) + '\n'

    bot.send_message(chat_id=update.message.from_user.id, text=text)
    return ConversationHandler.END
    # #傳圖片給使用者
    # bot.send_photo(chat_id=update.message.from_user.id, photo=url)

    # #下載midi檔案
    # dbx.files_download_to_file('temp/' +text+ '.mid', '/i_Piano/' +text+ '.mid')
    # #傳midi給使用者
    # bot.send_document(chat_id=update.message.from_user.id, document=open('temp/' +text+ '.mid', 'rb'))