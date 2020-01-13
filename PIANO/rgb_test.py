import mido
import pygame.midi
import midiutil
from midiutil.MidiFile3 import MIDIFile
import cv2
from primesense import openni2
from primesense import _openni2 as c_api
import pandas as pd
import numpy as np

dist = 'D:/program files/OpenNI2/Redist/'
## Initialize openni and check
openni2.initialize(dist)
if (openni2.is_initialized()):
    print("openNI2 initialized")
else:
    print("openNI2 not initialized")

dev = openni2.Device.open_any()
## Create the streams stream
rgb_stream = dev.create_color_stream()

rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=640, resolutionY=480, fps=30))

## Start the streams
rgb_stream.start()

def get_rgb():
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(480,640,3)
    rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    return rgb

if __name__ == '__main__':
    while 1:
        openni2.convert_depth_to_world
        rgb = get_rgb()
        cv2.imshow('rgb', rgb)