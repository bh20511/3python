

import tkinter as tk
import requests,json,os
from bs4 import BeautifulSoup

def download():
    url = entry1.get()
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html5lib')
    sticker_name = soup.find('p','mdCMN38Item01Ttl').text
    sticker_dir = sticker_name+"/"
    if not os.path.exists(sticker_dir):
        os.mkdir(sticker_dir)
    #抓每個貼圖-在li底下 以字串json方式呈現 所以之後要用json.loads讀入
    datas = soup.find_all('li','mdCMN09Li FnStickerPreviewItem')
    for data in datas:
        img_dic=json.loads(data['data-preview'])
        sticker_id = img_dic['id']
        img_file = requests.get(img_dic['staticUrl'])
        full_path =sticker_dir+sticker_id+".png"
        with open(full_path,"wb") as file:
            file.write(img_file.content)
        
win = tk.Tk()
win.title('line貼圖下載器')
win.geometry('600x150')
win.resizable(width=False,height=False)

label1 = tk.Label(win,text='請輸入Line貼圖網址',font=('Arial',20))
entry1 = tk.Entry(win,font=('Arial',16),bd=5,width="500")
button1 = tk.Button(win,text='下載',font=('Arial',16),fg='green',width=10,height=2,command=download)
label1.pack()
entry1.pack()
button1.pack()
win.mainloop()






