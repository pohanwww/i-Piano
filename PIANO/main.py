import mido
import pygame.midi
import midiutil
from midiutil.MidiFile3 import MIDIFile
import cv2
from primesense import openni2
from primesense import _openni2 as c_api
import pandas as pd
import numpy as np
import time
import sys
import subprocess
import tkinter

keys_down = []
key = cv2.waitKey(1) & 255

def print_devices():
    for n in range(pygame.midi.get_count()):
        print(n, pygame.midi.get_device_info(n))

def open_file(path):
    cmd = {'linux':'eog', 'win32':'explorer', 'darwin':'open'}[sys.platform]
    subprocess.run([cmd, path])

def read_input(input_device):
    event = []
    start_time = time.time()
    while True:
        if time.time() - start_time > 20:
            for i in event:
                print(i)
            break
        if input_device.poll():
            event.append(input_device.read(1)[0])
    return event
            # data = event[0]
            # timestamp = event[1]
            # note_number = data[1]
            # velocity = data[2]
            # if velocity > 0 and note_number not in keys_down:
            #     keys_down.append(note_number)
            # elif velocity == 0 and note_number in keys_down:
            #     key_index = keys_down.index(note_number)
            #     del keys_down[key_index]
            # print(keys_down)
            # print(number_to_note(note_number))
            # if velocity == 112:
            #     print('on')
            #     temp = timestamp
            # else:
            #     print('off', timestamp - temp)

def number_to_note(number):
    print("converting{0}".format(number))
    notes = ['c', 'c+', 'd', 'd+', 'e', 'f', 'f+', 'g', 'g+', 'a', 'a+', 'b']
    return notes[number % 12]

def to_midi(events):
    midistream = MIDIFile(1)
     
    track = 0   
    time = 0
    channel = 0
    volume = 100

    midistream.addTrackName(track, time, "Track")
    midistream.addTempo(track, time, 60)
    
    temp = []
    for event in events:
        if event[0][0] == 144: #key down
            temp = event
        elif event[0][0] == 128: #key up
            duration = (event[1] - temp[1])/1000
            pitch = event[0][1]
            time = temp[1]/1000
            midistream.addNote(track, channel, pitch, time, duration, volume)
            

    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midistream.writeFile(binfile)
    print(midistream)
    binfile.close()
    open_file('output.mid')

if __name__ == '__main__':
    pygame.midi.init()
    print_devices()
    piano_input = pygame.midi.Input(pygame.midi.get_default_input_id())
    events = read_input(piano_input)
    piano_input.close()

    to_midi(events)

# midistream = MIDIFile(1)
     
# track = 0   
# time = 0
# channel = 0
# volume = 100

# midi.addTrackName(track, time, "Track")
# midi.addTempo(track, time, 140)

# for note_group in note_groups:
#     duration = None
#     for note in note_group:
#         note_type = note.sym
#         if note_type == "1":
#             duration = 4
#         elif note_type == "2":
#             duration = 2
#         elif note_type == "4,8":
#             duration = 1 if len(note_group) == 1 else 0.5
#         pitch = note.pitch
#         midi.addNote(track, channel, pitch, time, duration, volume)
#         time += duration

# midi.addNote(track, channel, pitch, time, 4, 0)
# # And write it to disk.
# binfile = open("output.mid", 'wb')
# midi.writeFile(binfile)
# print(midi)
# binfile.close()
# open_file('output.mid')