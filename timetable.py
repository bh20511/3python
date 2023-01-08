import requests
from bs4 import BeautifulSoup
import tkinter as tk
import time
from tkcalendar import DateEntry

#爬蟲部分


#定義查詢功能(爬蟲技術為主)
def getTrip():
    listbox.delete(0,tk.END)
    url = 'https://www.railway.gov.tw/tra-tip-web/tip'
    #把要輸入表單的 日期、起訖站跟時間 都先取出來
    go = op12.get()
    arrive = op22.get()
    whichday = day.get()
    sTime = op3.get()
    eTime = op4.get()
    
    response = requests.get(url)
    if response.status_code != 200:
        listbox.insert(tk.END,'發生錯誤')
        return
    soup= BeautifulSoup(response.text,'html5lib')
           
    csrf = soup.find(id = 'queryForm').input['value']
    formData = {
        'trainTypeList': 'ALL',
        'transfer': 'ONE',
        'startOrEndTime': 'true',
        'startStation': go,
        'endStation': arrive,
        'rideDate': whichday,
        'startTime': sTime,
        'endTime': eTime,
        '_csrf':csrf
     }
    query_url='https://www.railway.gov.tw'+soup.find(id ="queryForm")['action']
    query_response = requests.post(query_url,data=formData) 
    qsoup = BeautifulSoup(query_response.text,'html5lib')
    trains = qsoup.find_all('tr','trip-column')
    
    for train in trains:
        tds = train.find_all('td')
        name = tds[0].ul.li.a.text
        start_time = tds[1].text
        arrive_time = tds[2].text
        spend_time = tds[3].text
        if op5.get()=='對號':
            if name[0:2]!='區間':
                listbox.insert(tk.END,f'車種:{name},出發時間:{start_time},抵達時間:{arrive_time},搭乘時間:{spend_time}')
        else:
            listbox.insert(tk.END,f'車種:{name},出發時間:{start_time},抵達時間:{arrive_time},搭乘時間:{spend_time}')
    if len(listbox.get(0))==0:
        listbox.insert(tk.END,'查無列車資訊')

#這邊只是要製作時刻的按鈕選項(因為懶地用手打,所以直接用爬蟲去抓)
url = 'https://www.railway.gov.tw/tra-tip-web/tip'
response = requests.get(url)
soup= BeautifulSoup(response.text,'html5lib')
clock = []
times = soup.find(id = 'startTime').find_all('option')
for i in times:
    clock.append(i.text)
        



#tkinter部分
#兩層式下拉式選單
def change_option_1(value):
	global first_option2
	first_option2.destroy()
	first_option2 = tk.OptionMenu(win,op12,*station[value])
	first_option2.place(x=450, y=20)
	op12.set(station[value][0])

def change_option_2(value):
    global second_option2
    second_option2.destroy()
    second_option2 = tk.OptionMenu(win,op22,*station[value])
    second_option2.place(x=450, y=80)
    op22.set(station[value][0])
   

city = (['基隆市','新北市','臺北市','桃園市','新竹縣','新竹市','苗栗縣','臺中市','彰化縣',
         '南投縣','雲林縣','嘉義縣','嘉義市','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣'])

station = {'基隆市':['0900-基隆','0910-三坑','0920-八堵','0930-七堵','0940-百福','7361-海科館','7390-暖暖'],
           '新北市':['0950-五堵','0960-汐止','0970-汐科','1020-板橋','1030-浮洲','1040-樹林','1050-南樹林','1060-山佳','1070-鶯歌','7290-福隆','7300-貢寮','7310-雙溪','7320-牡丹','7330-三貂嶺','7331-大華','7332-十分','7333-望古','7334-嶺腳','7335-平溪','7336-菁桐','7350-猴硐','7360-瑞芳','7362-八斗子','7380-四腳亭'],
           '臺北市':['1000-臺北','0980-南港','0990-松山','1010-萬華'],
           '桃園市':['1080-桃園','1090-內壢','1100-中壢','1110-埔心','1120-楊梅','1130-富岡','1140-新富'],
           '新竹縣':['1150-北湖','1160-湖口','1170-新豐','1180-竹北','1193-竹中','1194-六家','1201-上員','1202-榮華','1203-竹東','1204-橫山','1205-九讚頭','1206-合興','1207-富貴','1208-內灣'],
           '新竹市':['1210-新竹','1190-北新竹','1191-千甲','1192-新莊','1220-三姓橋','1230-香山'],
           '苗栗縣':['3160-苗栗','1240-崎頂','1250-竹南','2110-談文','2120-大山','2130-後龍','2140-龍港','2150-白沙屯','2160-新埔','2170-通霄','2180-苑裡','3140-造橋','3150-豐富','3170-南勢','3180-銅鑼','3190-三義'],
           '臺中市':['3300-臺中','2190-日南','2200-大甲','2210-臺中港','2220-清水','2230-沙鹿','2240-龍井','2250-大肚','2260-追分','3210-泰安','3220-后里','3230-豐原','3240-栗林','3250-潭子','3260-頭家厝','3270-松竹','3280-太原','3290-精武','3310-五權','3320-大慶','3330-烏日','3340-新烏日','3350-成功'],
           '彰化縣':['3360-彰化','3370-花壇','3380-大村','3390-員林','3400-永靖','3410-社頭','3420-田中','3430-二水','3431-源泉'],
           '南投縣':['3432-濁水','3433-龍泉','3434-集集','3435-水里','3436-車埕'],
           '雲林縣':['3450-林內','3460-石榴','3470-斗六','3480-斗南','3490-石龜'],
           '嘉義縣':['4050-大林','4060-民雄','4090-水上','4100-南靖'],
           '嘉義市':['4080-嘉義''4070-嘉北'],
           '臺南市':['4220-臺南','4110-後壁','4120-新營','4130-柳營','4140-林鳳營','4150-隆田','4160-拔林','4170-善化','4180-南科','4190-新市','4200-永康','4210-大橋','4250-保安','4260-仁德','4270-中洲','4271-長榮大學','4272-沙崙'],
           '高雄市':['4400-高雄','4290-大湖','4300-路竹','4310-岡山','4320-橋頭','4330-楠梓','4340-新左營','4350-左營','4360-內惟','4370-美術館','4380-鼓山','4390-三塊厝','4410-民族','4420-科工館','4430-正義','4440-鳳山','4450-後庄','4460-九曲堂'],
           '屏東縣':['4470-六塊厝','5000-屏東','5010-歸來','5020-麟洛','5030-西勢','5040-竹田','5050-潮州','5060-崁頂','5070-南州','5080-鎮安','5090-林邊','5100-佳冬','5110-東海','5120-枋寮','5130-加祿','5140-內獅','5160-枋山'],
           '臺東縣':['6000-臺東','5190-大武','5200-瀧溪','5210-金崙','5220-太麻里','5230-知本','5240-康樂','6010-山里','6020-鹿野','6030-瑞源','6040-瑞和','6050-關山','6060-海端','6070-池上'],
           '花蓮縣':['7000-花蓮','6080-富里','6090-東竹','6100-東里','6110-玉里','6120-三民','6130-瑞穗','6140-富源','6150-大富','6160-光復','6170-萬榮','6180-鳳林','6190-南平','6200-林榮新光','6210-豐田','6220-壽豐','6230-平和','6240-志學','6250-吉安','7010-北埔','7020-景美','7030-新城','7040-崇德','7050-和仁','7060-和平'],
           '宜蘭縣':['7190-宜蘭','7070-漢本','7080-武塔','7090-南澳','7100-東澳','7110-永樂','7120-蘇澳','7130-蘇澳新','7150-冬山','7160-羅東','7170-中里','7180-二結','7200-四城','7210-礁溪','7220-頂埔','7230-頭城','7240-外澳','7250-龜山','7260-大溪','7270-大里','7280-石城']           
           }


#基本設定(設定視窗名稱跟大小)
win = tk.Tk()
win.title('火車訂票系統')
win.geometry('760x768+800+80')
win.config(bg='ForestGreen')
win.resizable(0,0)

#起站設定    
label1 = tk.Label(win,text='起       站',font=('Arial',18))
label1.place(x=150, y=20)

op11 = tk.StringVar()
op11.set('桃園市')
first_option1 = tk.OptionMenu(win,op11, *city, command=change_option_1)
first_option1.place(x=300, y=20)
op12 = tk.StringVar()
op12.set('1080-桃園')
first_option2 = tk.OptionMenu(win,op12,*station[op11.get()])
first_option2.place(x=450, y=20)

#訖站設定
label2 = tk.Label(win,text='訖       站',font=('Arial',18))
label2.place(x=150, y=80)
op21 = tk.StringVar()
op21.set('桃園市')
second_option1 = tk.OptionMenu(win,op21, *city, command=change_option_2)
second_option1.place(x=300, y=80)
op22 = tk.StringVar()
op22.set('1080-桃園')
second_option2 = tk.OptionMenu(win,op22,*station[op21.get()])
second_option2.place(x=450, y=80)

#日期設定
label3 = tk.Label(win,text='日       期',font=('Arial',18))
label3.place(x=150, y=140)

today = time.strftime('%Y/%m/%d').split('/')
day = DateEntry(win, year=int(today[0]), month=int(today[1]), day=int(today[2]),date_pattern='Y/M/dd')
day.place(x=300 ,y=140)

#時間範圍
label4 = tk.Label(win,text='發車時段',font=('Arial',18) )
label4.place(x=150, y=200)
op3 = tk.StringVar()
op3.set('09:00')
third_option = tk.OptionMenu(win,op3,*clock)
third_option.place(x=300, y=200)

label4 = tk.Label(win,text='至',font=('Arial',18))
label4.place(x=400, y=200)
op4 = tk.StringVar()
op4.set('12:00')
fourth_option = tk.OptionMenu(win,op4,*clock)
fourth_option.place(x=450, y=200)  
#車種選擇
label5 = tk.Label(win,text='車種選擇',font=('Arial',18))
label5.place(x=150, y=260)
op5 = tk.StringVar()
op5.set('全部車種')
fifth_option =tk.OptionMenu(win,op5,'對號','全部車種')
fifth_option.place(x=300 ,y=260)  

#查詢按鈕
button = tk.Button(win,text='查詢',font=('Arial',16),width=8,height=1,relief='solid',command=getTrip)
button.place(x=150 ,y=320) 

#查到的資料 列在下面
frame =tk.Frame(win)
frame.place(x=0, y=400)
frame.config(bg='blue')

sbar = tk.Scrollbar(frame)
sbar.pack(side=tk.RIGHT,fill=tk.Y)

listbox = tk.Listbox(frame,font=('Arial',16),bg='bisque3',yscrollcommand=sbar.set,width=62,height=15)
listbox.pack()
sbar.config(command=listbox.yview)



win.mainloop()


