from tkinter.constants import E, N, RAISED, S, W
from typing import Text
import tkinter as tk
from SerialArduino import *
from datetime import date,datetime
import matplotlib.pyplot as plt
import numpy as np
import continuous_threading
import sys
from tkinter import messagebox
from tkinter import ttk
import copy

ser = Serial_Arduino("COM5",9600)

window = tk.Tk()
#window.iconbitmap("E:/lock.png")
window.title("Project")
#window.geometry("500x200")
window.resizable(0,0)

day_set = 0
num_hour = 0
engle_current = 0
n=0
data = ""
x=[]
y=[]
T = tk.StringVar()
H = tk.StringVar()
E = tk.StringVar()
date_today = tk.StringVar()
time_current = tk.StringVar()

#day_poin = tk.StringVar()
hour_poin = tk.StringVar()
minute_poin = tk.StringVar()
#day_poin.set("01")
hour_poin.set("00")
minute_poin.set("00")

E.set("0")

def write_file():
    file_object = open('D:\project pyserial\Project\data.txt',mode='r+')
    data = file_object.readline()
    T_str = data[0]
    poin = data[1]
    

def hour_minute(time):
    num1 = time.split(":")
    hour = num1[0]
    minute = num1[1]
    return hour,minute

def get_datetime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    date_object = date.today()
    return current_time,date_object
    
def check_file():
    global data
    file_object = open('D:\project pyserial\Project\data.txt',mode='r+')
    data = file_object.read()
    if data == "":
        file_object.close()
        return 0

def save_data(): #func cho button save data current
    file_object= open('D:\project pyserial\Project\data.txt',mode='r+')
    data = file_object.read()
    print(data)
    file_object.close()
    messagebox.showinfo("Notify","Done saver!")

def save_poin():
    #day_poin_str = spin_box1.get()
    hour_poin_str = spin_box2.get()
    minute_poin_str = spin_box3.get()
    print(hour_poin_str,minute_poin_str)
    #print(day_poin_str,hour_poin_str,minute_poin_str)
    #messagebox.showinfo("Notify","Done saver!")

def draw():
    global data,y,x
    check = check_file()
    if check == 0:
        messagebox.showerror("Erorr","Don't have data!")
    else:
        data_list = data.split("\n")
        T_str = data_list[0]
        M_str = data_list[1]
        T_str2 = T_str.split(",")
        M_str2 = M_str.split(",")
        for i in range (len(T_str2)):
            x.append(int(M_str2[i]))
            y.append(int(T_str2[i]))
        plt.axis([0,30,5,45])
        plt.xlabel("Poin")
        plt.ylabel("Temperature")
        plt.plot(x,y,"r")
        plt.plot(x,y,"ok")
        plt.show()
        messagebox.showinfo("Notify","Biên độ nhiệt: "+str(max(y)-min(y)))

def write_data(engle):
    global engle_current
    if(engle_current + engle) <= 180 and (engle_current + engle) >= 0:
        engle_current += engle
        ser.write_data(engle_current)
    E.set(str(engle_current))

def readserial():
    global day_set
    global num_hour
    global n
    ser_str = ser.get_data()
    T.set(ser_str[0])
    H.set(ser_str[1])

    num = get_datetime()
    num_coppy = copy.copy(num)
    num_time = hour_minute(num_coppy[0])
    if n == 0: 
        num_hour = num_time[0]
        n+=1
    print(num_hour)

    date_today.set(num[1])
    time_current.set(num[0])

    time.sleep(0.2)

t1 = continuous_threading.PeriodicThread(0.2, readserial)

def exit_all():
    ser.close_port()
    sys.exit()

frame_sensor = tk.Frame(window,padx=100,pady=20,relief=RAISED,border=2)
frame_sensor.grid(column=0,row=0)
frame_servo = tk.Frame(window,width=250,height=200,relief=RAISED,border=2)
frame_servo.grid(column=0,row=1)

lb_T = tk.Label(frame_sensor,text="Temperature: ",anchor=W,width=10)
lb_T.grid(column=0,row=0)
lb1 = tk.Label(frame_sensor,text="%",padx=42)
lb1.grid(column=1,row=0,sticky=W)
et_showH = tk.Entry(frame_sensor,textvariable=H,width=5,state="disabled")
et_showH.grid(column=1,row=0,sticky=W,padx=5)

lb_H = tk.Label(frame_sensor,text="Humidity: ",anchor=W,width=10)
lb_H.grid(column=0,row=1)
lb2 = tk.Label(frame_sensor,text="°C",padx=40)
lb2.grid(column=1,row=1,sticky=W)
et_showT = tk.Entry(frame_sensor,textvariable=T,width=5,state="disabled")
et_showT.grid(column=1,row=1,sticky=W,padx=5)

et_showtime = tk.Entry(frame_sensor,textvariable=time_current,state="disabled",width=8)
et_showtime.grid(column=3,row=0,sticky=W,padx=5)
et_showdate = tk.Entry(frame_sensor,textvariable=date_today,state="disabled",width=10)
et_showdate.grid(column=2,row=0,sticky=W,padx=5)

b_savepoin = tk.Button(frame_sensor,text="Save poin",command=save_poin)
b_savepoin.grid(column=2,row=2,padx=5,pady=5)

""" spin_box1 = ttk.Spinbox(frame_sensor,from_=0,to=30,textvariable=day_poin,wrap=True,width=4)
spin_box1.grid(column=2,row=1,sticky=W,padx=5) """
spin_box2 = ttk.Spinbox(frame_sensor,from_=0,to=24,textvariable=hour_poin,wrap=True,width=6)
spin_box2.grid(column=3,row=1,sticky=W,padx=5)
spin_box3 = ttk.Spinbox(frame_sensor,from_=1,to=60,textvariable=minute_poin,wrap=True,width=4)
spin_box3.grid(column=4,row=1,sticky=W,padx=0)

b_Get=tk.Button(frame_sensor,text="Save data current",command=save_data)
b_Get.grid(column=0,row=2,padx=5,pady=10)
b_draw = tk.Button(frame_sensor,text="Temperature fluctuation graph",command=draw)
b_draw.grid(column=1,row=2,padx=5,pady=10)

lb_E = tk.Label(frame_servo,text="Engle current: ",anchor=W,width=10,padx=10,pady=10)
lb_E.grid(column=0,row=0)
lb3 = tk.Label(frame_servo,text="°",anchor="w")
lb3.grid(column=2,row=0,sticky="w",padx=0)
et_showE = tk.Entry(frame_servo,textvariable=E,width=4)
et_showE.grid(column=1,row=0)

b_servo1 = tk.Button(frame_servo,text="Turn left 45°",command=lambda:write_data(45))
b_servo1.grid(column=0,row=1,padx=5,pady=10)
b_servo2 = tk.Button(frame_servo,text="Turn right 45°",command=lambda:write_data(-45))
b_servo2.grid(column=3,row=1,padx=3,pady=10)
b_servo3 = tk.Button(frame_servo,text="Go home",command=lambda:write_data(-engle_current))
b_servo3.grid(column=1,row=1,padx=5,pady=10)

b_exit = tk.Button(window,text="Exit",command=exit_all,width=10)
b_exit.grid(column=0,row=2,padx=5,pady=5,sticky="e")
#-------------------------------------------------------------------------------------------
t1.start()
window.mainloop()