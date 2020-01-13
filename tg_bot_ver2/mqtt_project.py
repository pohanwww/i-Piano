import paho.mqtt.client as mqtt   #  pip install paho-mqtt
import time  
import json  
import random

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
MQTT_po_midi  = "po/midi_url/" 

songs = ["song1", "song2" , "song3" ,"song4"]

# *********************************************************************

song_names = ["小星星簡單板","小蜜蜂","小星星"] 

user_names = ["user1","user2","user3","user4"]

pic_urls = ["https://i.postimg.cc/4dw9N4j5/PtNQQuk.png",
	"https://i.postimg.cc/JzKcb2fB/YVCX87Q.png",
	"https://i.postimg.cc/BZDThbW3/xsxh1lx.png"]

fault_pic_urls = ["https://i.postimg.cc/L8rfBFy5/message-Image-15726072369171.jpg",
	"https://i.postimg.cc/L8rfBFy5/message-Image-15726072369171.jpg",
	"https://i.postimg.cc/L8rfBFy5/message-Image-15726072369171.jpg",
	"https://i.postimg.cc/L8rfBFy5/message-Image-15726072369171.jpg"]

# *********************************************************************

mqtt_client = mqtt.Client()  
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)    
score = [20, 20, 20, 20]
for i in range(10):

	for i, pic_url in enumerate(pic_urls): 
		mqtt_client.publish( MQTT_po_pic + str(i+1) , pic_url ) # 正確五線譜
	for i, song_name in enumerate(song_names):
		mqtt_client.publish( MQTT_po_song + str(i+1) , song_name) #首頁樂譜名稱

	for i, user_name in enumerate(user_names):
		mqtt_client.publish( MQTT_po_user + str(i+1) , user_name ) # 使用者姓名
		# mqtt_client.publish( MQTT_po_song + str(i+1) , song_names[i] ) # 曲名
	
	for i, song in enumerate(songs):
		for k in range(4):
			#print(k)
			score[k] += random.randint(-3,6)
			if score[k] > 100:
				score[k] = 100
			print(score[k])
			mqtt_client.publish( MQTT_po + song + MQTT_po_score + str(k+1) , score[k] ) # 全部使用者每首分數
			#mqtt_client.publish( MQTT_po + song + "/s/" + str(k+1) , random.random())	

	for i, song in enumerate(songs):
		for k in range(4):
			mqtt_client.publish( MQTT_po_midi+ song + "/" + str(k+1) , fault_pic_urls[k] )  # 評分url

	time.sleep(3)


#******************************
# for i, pic_url in enumerate(pic_urls): 
# 		mqtt_client.publish( MQTT_po_pic + str(i+1) , pic_url ) # 正確五線譜
# for i, song_name in enumerate(song_names):
# 	mqtt_client.publish( MQTT_po_song + str(i+1) , song_name) #首頁樂譜名稱

# for i, user_name in enumerate(user_names):
# 	mqtt_client.publish( MQTT_po_user + str(i+1) , user_name ) # 使用者姓名
# 	# mqtt_client.publish( MQTT_po_song + str(i+1) , song_names[i] ) # 曲名

# for i, song in enumerate(songs):
# 	for k in range(4):
# 		#print(k)
# 		mqtt_client.publish( MQTT_po + song + MQTT_po_score + str(k+1) , random.randint(0,100) ) # 全部使用者每首分數
# 		#mqtt_client.publish( MQTT_po + song + "/s/" + str(k+1) , random.random())	

# for i, song in enumerate(songs):
# 	for k in range(4):
# 		mqtt_client.publish( MQTT_po_midi+ song + "/" + str(k+1) , fault_pic_urls[k] )  # 評分url