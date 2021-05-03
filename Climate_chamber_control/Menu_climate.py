#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 27 15:05:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
import tkinter as tk
from tkinter import *
import Climate_chamber


# =============================================================================

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
                            command=lambda: [Climate_chamber.cycle(scale1.get(), 0)])
        button1.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
        button2 = tk.Button(my_settings_chamber_frame, text="Quit",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [sys.exit()])
        button2.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)
        button3 = tk.Button(my_settings_chamber_frame, text="Off",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [Climate_chamber.cycle(scale1.get(), 1)])
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
                             variable=b, value=0, cursor="right_ptr", command=lambda: [scale3.configure(state="disabled")])
        RB1.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        RB2 = tk.Radiobutton(my_settings_chamber_frame, text="multi_cycles",
                             variable=b, value=1, cursor="right_ptr", command=lambda: [scale3.configure(state="active")])
        RB2.grid(row=1, column=2, ipadx=40, ipady=40, padx=0, pady=0)
        scale3 = Scale(my_settings_chamber_frame, orient='horizontal', troughcolor=elcolor, from_=0, to=20,
                       resolution=1, tickinterval=5, length=100, command=0,
                       label='nomber of cycles', state="disabled", relief="flat")
        scale3.grid(row=2, column=1, ipadx=40, ipady=40, padx=0, pady=0)


Climate().mainloop()
