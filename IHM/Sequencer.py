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
from IHM_piloting.EA import Button_jump
import IHM_piloting.EA.Button_jump

# =============================================================================
THE_COLOR = "#E76145"


def sequencer(self):
    global number_box
    number_box = int()
    global list
    list = {}

    def show_menu(e):
        menu_base.post(e.x_root, e.y_root)

    def show_menu_box(e):
        global box
        menu_box.post(e.x_root, e.y_root)
        word = str(e.widget)
        try:
            number = int(word[-1:])-1
        except:
            number = 0
        box = number

    sequencer_frame = LabelFrame(self, text="Sequencer frame")
    sequencer_frame.grid(row=0, column=2, ipadx=40, ipady=40, padx=0, pady=0, rowspan=1)
    board_frame = LabelFrame(self, text="Board")
    board_frame.grid(row=0, column=3, ipadx=40, ipady=40, padx=0, pady=0, rowspan=4)
    board_frame.grid_forget()
    sequencer_label = tk.Label(sequencer_frame, text="Sequencer frame", bg="white", font="arial",
                               fg="black", relief="groove")
    sequencer_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    sequencer_add_label = tk.Label(sequencer_frame, text="Add", bg=THE_COLOR, font="arial",
                                   fg="black", relief="groove", cursor="right_ptr")
    sequencer_add_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    sequencer_start_button = tk.Button(sequencer_frame, text="Launch",
                                       borderwidth=8, background=THE_COLOR,
                                       activebackground="green", cursor="right_ptr", overrelief="sunken",
                                       command=lambda: [])
    sequencer_start_button.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)

    menu_base = tkinter.Menu(self, tearoff=0)

    submenu_1 = Menu(menu_base)
    submenu_1.add_command(label="Climatic chamber", command=lambda: [board_add(board_frame, "Climatic chamber")])
    submenu_1.add_command(label="SMIQ", command=lambda: [board_add(board_frame, "SMIQ")])
    menu_base.add_cascade(label='Add', menu=submenu_1, underline=0)
    """
    submenu_2 = Menu(menu_base)
    submenu_2.add_command(label="Climatic chamber")
    submenu_2.add_command(label="SMIQ")
    menu_base.add_cascade(label='Remove', menu=submenu_2, underline=0)
    """
    sequencer_add_label.bind("<Button-1>", show_menu)
    sequencer_label.bind("<Button-2>", IHM_piloting.EA.Button_jump.play)

    menu_box = tkinter.Menu(self, tearoff=0)
    menu_box.add_command(label="Delete ", command=lambda: [delete_box(box)])
    menu_box.add_command(label="Move up ", command=lambda: [move_up_box(box)])
    menu_box.add_command(label="Move down  ", command=lambda: [move_down_box(box)])

    def board_add(board_frame, name):
        global number_box
        if not (board_frame.winfo_manager() == "grid"):
            board_frame.grid(row=0, column=3, ipadx=40, ipady=40, padx=0, pady=0, rowspan=2)
            number_box = 0
        else:
            number_box = number_box + 1
        create_box(board_frame, number_box, name)

    def create_box(board_frame, number_box, name):
        global list
        var = number_box
        a = tk.Label(board_frame, text=str(number_box) + " : " + name + "      ⚙", bg="white", font="arial",
                              fg="black", relief="groove")
        a.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
        list[var] = a
        a.bind("<Button-1>", show_menu_box)

    def move_up_box(box):
        print(f"Move up {box}")

    def move_down_box(box):
        print(f"Move down {box}")

    def delete_box(box):
        global list
        list[box].destroy()
