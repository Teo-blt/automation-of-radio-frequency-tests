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
from EA import Button_jump
import EA.Button_jump

# =============================================================================
THE_COLOR = "#E76145"


def sequencer(self):
    def show_day():
        now = datetime.datetime.now()
        msg = 'Today is: {}'.format(now.strftime('%A'))
        tkinter.messagebox.showinfo("Information", msg)

    def show_menu(e):
        menu_base.post(e.x_root, e.y_root)

    sequencer_frame = LabelFrame(self, text="Sequencer frame")
    sequencer_frame.grid(row=0, column=2, ipadx=40, ipady=40, padx=0, pady=0, rowspan=4)
    sequencer_label = tk.Label(sequencer_frame, text="Sequencer frame", bg="white", font="arial",
                               fg="black", relief="groove")
    sequencer_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    sequencer_add_label = tk.Label(sequencer_frame, text="Add", bg=THE_COLOR, font="arial",
                                   fg="black", relief="groove", cursor="right_ptr")
    sequencer_add_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)

    menu_base = tkinter.Menu(self, tearoff=0)
    menu_base.add_command(label="Show day", command=show_day)

    submenu_1 = Menu(menu_base)
    submenu_1.add_command(label="Climatic chamber")
    submenu_1.add_command(label="SMIQ")
    menu_base.add_cascade(label='Add', menu=submenu_1, underline=0)

    submenu_2 = Menu(menu_base)
    submenu_2.add_command(label="Climatic chamber")
    submenu_2.add_command(label="SMIQ")
    menu_base.add_cascade(label='Remove', menu=submenu_2, underline=0)

    sequencer_add_label.bind("<Button-1>", show_menu)
    sequencer_label.bind("<Button-2>", EA.Button_jump.play)