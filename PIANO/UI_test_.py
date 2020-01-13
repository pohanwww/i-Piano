from tkinter import *
import time
import tkinter as tk
import pandas as pd
import numpy as numpy
import imgur_downloader
import dropbox, sys, os
from dropbox.files import WriteMode
import cv2
from PIL import Image, ImageTk
import mido
import pygame.midi
import midiutil
from midiutil.MidiFile3 import MIDIFile
import sys
import subprocess

dbx = dropbox.Dropbox('jgH_djvkJasAAAAAAAAAFQslYkn9coLtRYvDeXQtXevRFR5WBAeHp42ZuLzUAly0')

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
    for event_ in events_:
        if event_[0][0] == 144: #key down
            temp = event_
        elif event_[0][0] == 128: #key up
            duration = (event_[1] - temp[1])/1000
            pitch = event_[0][1]
            time = temp[1]/1000
            midistream.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midistream.writeFile(binfile)
    print(midistream)
    binfile.close()
    # open_file('output.mid')

def video_loop():
    success, img = camera.read()  # 從攝像頭讀取照片
    if success:
        cv2.waitKey(20)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
        current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)
        
class Practice(Frame):
    msec = 50
    tempo_count = 1
    tempo = 0
    flipflop = False
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.flag  = True
        self._running = False
    def search_img(self, song_name):
        text = song_name
        dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
        df = pd.read_csv('temp/music_list.csv', index_col=False)
        img_url = df.loc[df['music_name'] == text]['music_sheet_url'].values[0]
        imgur_downloader.ImgurDownloader(imgur_url=img_url, file_name='song_img').save_images('image')

    def layout(self):
        if self.flag == True:
        #介面設定
            label = tk.Label(root, text="这是第一页", font=('Arial', 20))
            label.pack(pady=10,padx=10)
            label = tk.Label(root, text="Tempo:", font=('Arial', 28))
            label.place(x=60, y=120)
            tempo_var = tk.StringVar()
            tempo_entry = tk.Entry(root, textvariable=tempo_var, show=None, font=('Arial', 28), width=20)  # 顯示成明文形式
            tempo_entry.place(x=60, y=175)
            start_button = tk.Button(root, text='Start', font=('Arial', 28), width=18, height=1, command=lambda: self._start(int(tempo_var.get())))
            start_button.place(x=60, y=240)
            stop_button = tk.Button(root, text='Stop', font=('Arial', 28), width=18, height=1, command=lambda: self._stop())
            stop_button.place(x=60, y=330)

            #載入圖片
            load = Image.open("image/song_img.jpg")
            render = ImageTk.PhotoImage(load)
            img = Label(root, image=render)
            img.image = render
            img.pack()
        self.flag = False

    def prepare(self, song_name, user_name):
        frame1.destroy()
        label_1.destroy()
        label_2.destroy()
        search_entry.destroy()
        user_entry.destroy()
        search_button.destroy()
        self.search_img(song_name)
        self.layout()

    def _update(self):
        Metronome = tk.Label(root, bg='white', width=50, height=50)
        Metronome.place(x=1360, y=80)
        if piano_input.poll():
            event.append(piano_input.read(1)[0])
        if self.tempo_count % (self.tempo//6) == 0:
            self.flipflop = not self.flipflop
        if self.flipflop == True:
            Metronome.config(bg='yellow')
        else:
            Metronome.config(bg='white')
        # Metronome = tk.Label(self, bg='yellow', width=50, height=50)
        # Metronome.place(x=1360, y=80)
        self.tempo_count += 1
        self.timer = self.after(self.msec, self._update)

    def _start(self, tempo_):
        if not self._running:
            self.tempo = tempo_
            self._update()
            self._running = True
    def _stop(self):
        if self._running:
            self._running = False
        for i in event:
            print(i)
        to_midi(event)
        # print(i for i in event)

root = Tk()
root.geometry('{}x{}'.format(root.maxsize()[0], root.maxsize()[1]))
frame1 = Frame(root, width=root.maxsize()[0]/2, height=root.maxsize()[1]/3)
frame1.pack()
prac = Practice(root)
label_1 = tk.Label(root, text="使用者名稱：", font=('Arial', 32))
label_1.pack()
user_name_str = tk.StringVar()
user_entry = tk.Entry(root, textvariable=user_name_str, show=None, font=('Arial', 32), width=40)  # 顯示成明文形式
user_entry.pack()
label_2 = tk.Label(root, text="請輸入曲目名稱：", font=('Arial', 32))
label_2.pack()
song_name_str = tk.StringVar()
search_entry = tk.Entry(root, textvariable=song_name_str, show=None, font=('Arial', 32), width=40)  # 顯示成明文形式
search_entry.pack()
search_button = tk.Button(root, text='search', font=('Arial', 32), width=38, height=1, command=lambda: prac.prepare(song_name_str.get(), user_name_str.get()))
search_button.pack()

event = []
pygame.midi.init()
piano_input = pygame.midi.Input(pygame.midi.get_default_input_id())

if __name__ == '__main__':
    
    root.mainloop()