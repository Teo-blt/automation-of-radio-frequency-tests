import threading
import time
import tkinter as tk
from tkinter import *
import sys


# test of the functioning of the threading

class Mythread(threading.Thread):
    def __init__(self, data):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.data = data  # additional data added to the class

    def run(self):
        for i in range(0, 100):
            print("thread ", i)
            time.sleep(1)  # wait 100 milliseconds without doing anything,  makes the display easier to read


m = Mythread(10)  # build the thread
m.start()  # lunch the thread,


# instruction is executed in milliseconds, whatever the length of the thread


# __Main__
class Climate(Tk):
    def __init__(self):
        Tk.__init__(self)
        global elcolor
        elcolor = "#E76145"
        self.settings_chamber()

    def settings_chamber(self):  # creation of a lobby menu
        b = IntVar()
        my_settings_chamber_frame = LabelFrame(self, text="Choice of instrument")
        my_settings_chamber_frame.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        label = tk.Label(my_settings_chamber_frame, text="Settings_chamber", bg="white", font="arial",
                         fg="black", relief="groove")
        label.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        button1 = tk.Button(my_settings_chamber_frame, text="Start",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [print("1")])
        button1.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
        button2 = tk.Button(my_settings_chamber_frame, text="Quit",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [self.quit(), self.destroy()])
        button2.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)
        button3 = tk.Button(my_settings_chamber_frame, text="Off",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [print("2")])
        button3.grid(row=0, column=3, ipadx=40, ipady=20, padx=0, pady=0)
        scale1 = Scale(my_settings_chamber_frame, orient='vertical', troughcolor=elcolor, from_=100, to=-20,
                       resolution=1, tickinterval=20, length=100, command=0,
                       label='temperature_min', state="active")
        scale1.grid(row=1, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        scale2 = Scale(my_settings_chamber_frame, orient='vertical', troughcolor=elcolor, from_=100, to=-20,
                       resolution=1, tickinterval=20, length=100, command=0,
                       label='temperature_max', state="active")
        scale2.grid(row=2, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        RB1 = tk.Radiobutton(my_settings_chamber_frame, text="mono_cycle",
                             variable=b, value=0, cursor="right_ptr",
                             command=lambda: [scale3.configure(state="disabled")])
        RB1.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        RB2 = tk.Radiobutton(my_settings_chamber_frame, text="multi_cycles",
                             variable=b, value=1, cursor="right_ptr",
                             command=lambda: [scale3.configure(state="active")])
        RB2.grid(row=1, column=2, ipadx=40, ipady=40, padx=0, pady=0)
        scale3 = Scale(my_settings_chamber_frame, orient='horizontal', troughcolor=elcolor, from_=0, to=20,
                       resolution=1, tickinterval=5, length=100, command=0,
                       label='nomber of cycles', state="disabled", relief="flat")
        scale3.grid(row=2, column=1, ipadx=40, ipady=40, padx=0, pady=0)


Climate().mainloop()
