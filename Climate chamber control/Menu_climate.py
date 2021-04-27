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
import os
from tkinter.messagebox import *
import tkinter as tk
import sys
from tkinter import *
from tkinter import ttk
# =============================================================================

class Climate(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.settings_chamber()

    def settings_chamber(self):  # creation of a lobby menu
        my_settings_chamber_frame = LabelFrame(self, text="Choice of instrument",bg="grey")
        my_settings_chamber_frame.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        label = tk.Label(my_settings_chamber_frame, text="Settings_chamber", )
        label.pack(padx=10, pady=10, expand=True, fill="both", side=TOP)
        button1 = tk.Button(my_settings_chamber_frame, text="Start",
                            borderwidth=8, background="red",
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [Climate chamber])
        button1.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button2 = tk.Button(my_settings_chamber_frame, text="Quit",
                            borderwidth=8, background="red",
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [sys.exit()])
        button2.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

Climate().mainloop()