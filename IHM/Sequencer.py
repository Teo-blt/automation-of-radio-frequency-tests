#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 2 11:25:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import tkinter as tk
from tkinter import *
import tkinter
import tkinter.messagebox
import datetime


# =============================================================================
def sequencer(self):

    def showday():
        now = datetime.datetime.now()
        msg = 'Today is: {}'.format(now.strftime('%A'))
        tkinter.messagebox.showinfo("Information", msg)

    def showmenu(e):
        pmenu.post(e.x_root, e.y_root)

    sequencer_frame = LabelFrame(self)
    sequencer_frame.grid(row=0, column=2, ipadx=40, ipady=40, padx=0, pady=0, rowspan=4)
    sequencer_label = tk.Label(sequencer_frame, text="Sequencer frame", bg="white", font="arial",
                               fg="black", relief="groove")
    sequencer_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    sequencer_label_2 = tk.Label(sequencer_frame, text="in progress...")
    sequencer_label_2.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)

    pmenu = tkinter.Menu(self, tearoff=0)
    pmenu.add_command(label="Show day", command=showday)
    pmenu.add_command(label="Exit", command=self.quit)
    self.bind("<Button-3>", showmenu)
