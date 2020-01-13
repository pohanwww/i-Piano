import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk  
import function
import pandas as pd
import numpy as numpy
import imgur_downloader
import dropbox, sys, os
from dropbox.files import WriteMode
import cv2

dbx = dropbox.Dropbox('jgH_djvkJasAAAAAAAAAFQslYkn9coLtRYvDeXQtXevRFR5WBAeHp42ZuLzUAly0')


class Application(tk.Tk):
    def __init__(self):
        
        super().__init__()

        # self.iconbitmap(default="kankan_01.ico")
        self.wm_title("多页面测试程序")
        window_w = self.maxsize()[0]
        window_h = self.maxsize()[1]
        self.geometry('{}x{}'.format(window_w, window_h))
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！

        self.show_frame(StartPage)
    
    def search_img(self, song_name):
        text = song_name
        dbx.files_download_to_file('temp/music_list.csv', '/i_Piano/music_list.csv')
        df = pd.read_csv('temp/music_list.csv', index_col=False)
        img_url = df.loc[df['music_name'] == text]['music_sheet_url'].values[0]
        imgur_downloader.ImgurDownloader(imgur_url=img_url, file_name='song_img').save_images('image')

        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # 切换，提升当前 tk.Frame z轴顺序（使可见）！！此语句是本程序的点睛之处

        
class StartPage(tk.Frame):
    '''主页'''
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="請輸入曲目名稱：", font=('Arial', 32))
        label.place(x=500, y=370)

        song_name_str = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=song_name_str, show=None, font=('Arial', 32), width=40)  # 顯示成明文形式
        search_entry.place(x=500, y=430)
        search_button = tk.Button(self, text='search', font=('Arial', 32), width=38, height=1, command=lambda: root.search_img(song_name_str.get()))
        search_button.place(x=503, y=500)

class PageOne(tk.Frame):
    '''第一页'''
    def __init__(self, parent, root):
        super().__init__(parent)
        #介面設定
        label = tk.Label(self, text="这是第一页", font=('Arial', 20))
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Tempo:", font=('Arial', 28))
        label.place(x=60, y=120)
        tempo = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=tempo, show=None, font=('Arial', 28), width=20)  # 顯示成明文形式
        search_entry.place(x=60, y=175)
        search_button = tk.Button(self, text='Start', font=('Arial', 28), width=18, height=1, command=lambda: self.start(tempo))
        search_button.place(x=60, y=240)

        #載入圖片
        load = Image.open("image/song_img.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.pack()
        
        
    
    def start(self, tempo):
        print(tempo.get())
        Metronome = tk.Label(self, bg='yellow', width=50, height=50)
        Metronome.place(x=1360, y=80)

if __name__ == '__main__':
    # 实例化Application
    app = Application()
    app.mainloop()
    