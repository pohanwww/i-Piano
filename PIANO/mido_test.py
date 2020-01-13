import mido
from mido import MidiFile, Message, tempo2bpm, MidiTrack,MetaMessage
import datetime
import signal
import time
import sys
mid = mido.MidiFile('output.mid')
print(mid)

for i, track in enumerate(mid.tracks):
    print('Track name', track.name)
    for index, msg in enumerate(track):
        print('msg{}'.format(index), msg)
    

