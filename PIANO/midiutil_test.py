import midiutil
from midiutil.MidiFile3 import MIDIFile
import subprocess
import mido
import sys
import dropbox
from dropbox.files import WriteMode
import paho.mqtt.client as mqtt   #  pip install paho-mqtt

dbx = dropbox.Dropbox('jgH_djvkJasAAAAAAAAAFQslYkn9coLtRYvDeXQtXevRFR5WBAeHp42ZuLzUAly0')

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

def open_file(path):
    cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
    subprocess.run([cmd, path])

def to_midi(events_):
    midistream = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100

    midistream.addTrackName(track, time, "Track")
    midistream.addTempo(track, time, 60)
    
    temp = []
    for index, event_ in enumerate(events_):
        if event_[0][0] == 144: #key down
            temp = event_
        elif event_[0][0] == 128: #key up
            duration = (event_[1] - temp[1])/1000
            pitch = event_[0][1]
            time = temp[1]/1000
            midistream.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    binfile = open("temp/user_output.mid", 'wb')
    midistream.writeFile(binfile)
    print(midistream)
    binfile.close()
    # open_file('output.mid')

events = [[[144, 72, 112, 0], 10000],
[[128, 72, 63, 0], 15000] ,
[[144, 72, 112, 0], 20000],
[[128, 72, 63, 0], 25000] ,
[[144, 72, 112, 0], 35000],
[[128, 72, 63, 0], 45000] ]

# to_midi(events)

mid = mido.MidiFile("temp/user_output.mid")

def mid_2_script(mid):
    script = []
    for track in mid.tracks:
        track_tempo = 0
        start_time = 0
        #find tempo
        for msg in track:
            if msg.type == 'set_tempo':
                track_tempo = msg.tempo
                print('track_tempo', track_tempo)
        #find start time
        for msg in track:
            if msg.type == 'note_on':
                start_time = msg.time
                print('start',start_time)
                break
        
        all_over_time = 0
        for index, msg in enumerate(track):
               #one_note = [note, bit, duration]
            if msg.type == 'note_on':
                one_note = [] 
                if start_time != msg.time:
                    all_over_time += msg.time
                for i in range(index, len(track)):
                    if (track[i].type == 'note_off'):
                        if (msg.note == track[i].note):
                            
                            one_note.append(msg.note)
                            one_note.append((all_over_time) / 960 + 1)
                            print(all_over_time)
                            one_note.append(track[i].time / 960)
                            all_over_time += track[i].time
                            # print(all_over_time)
                            print(one_note)
                            break
                script.append(one_note)
            elif msg.type == 'end_of_track':
                break
    return script

script = mid_2_script(mid)
# for i in script:
#     print(i)

# for i, track in enumerate(mid.tracks):
#     print('Track name', track.name)
#     for index, msg in enumerate(track):
#         print('msg{}'.format(index), msg)

# for i, track in enumerate(mid.tracks):
#     print('Track name', track.name)
#     full_track = []
#     duration = 0
#     bit = 0
#     note = None
#     first_note = track[0]
#     for index, msg in enumerate(track):
#         if msg[0] == 144: #key down
#             temp = event_
#         elif event_[0][0] == 128: #key up
#             duration = (event_[1] - temp[1])/1000
#             pitch = event_[0][1]
#             time = temp[1]/1000
#             midistream.addNote(track, channel, pitch, time, duration, volume)
