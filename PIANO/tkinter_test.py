import tkinter as tk  # 使用Tkinter前需要先匯入
import os
from PIL import Image, ImageTk  

def resize(w, h, w_box, h_box, pil_image):  
  ''' 
  resize a pil_image object so it will fit into 
  a box of size w_box times h_box, but retain aspect ratio 
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
  '''  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  #print(f1, f2, factor) # test  
  # use best down-sizing filter  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS)  


# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('Piano')
window.geometry('{}x{}'.format(window.maxsize()[0], window.maxsize()[1]))  # 這裡的乘是小x


# 第4步，在圖形介面上設定標籤
# var = tk.StringVar()    # 將label標籤的內容設定為字元型別，用var來接收hit_me函式的傳出內容用以顯示在標籤上
# l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)

# # 說明： bg為背景，fg為字型顏色，font為字型，width為長，height為高，這裡的長和高是字元的長和高，比如height=2,就是標籤有2個字元這麼高
# l.pack()


pil_image = Image.open(r'image/img_src.png')  
w, h = pil_image.size  
pil_image = resize(w, h, window.maxsize()[0], window.maxsize()[1], pil_image)  
tk_image = ImageTk.PhotoImage(pil_image)

label_img = tk.Label(window, image = tk_image)
label_img.pack()

# 定義一個函式功能（內容自己自由編寫），供點選Button按鍵時呼叫，呼叫命令引數command=函式名
on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
    else:
        on_hit = False
        var.set('')

# 第5步，在視窗介面設定放置Button按鍵
search_button = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
search_button.place(x=10, y=10, anchor='nw')

search_entry = tk.Entry(window, show=None, font=('Arial', 14))  # 顯示成明文形式
search_entry.place(x=10, y=40, anchor='nw')

# 第6步，主視窗迴圈顯示
window.mainloop()

