#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 2 14:30:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import random
import tkinter as tk
# =============================================================================

def play(e):

    def on_enter_button(e):
        w = root.winfo_width()
        h = root.winfo_height()

        b_w = btn.winfo_width()
        b_h = btn.winfo_height()

        r_x = random.randrange(0, w - b_w)
        r_y = random.randrange(0, h - b_h)

        btn.place(x=r_x, y=r_y)

    root = tk.Tk()
    root.title('Jumping button')
    label = tk.Label(root, text="Click on the button to exit the application", bg="grey",
                     font="arial", fg="black", relief="groove")
    label.pack(padx=1, pady=1, expand=True, fill="both")
    root.resizable(False, False)

    btn = tk.Button(root, text='Exit', width=10, borderwidth=8, background="#E76145",
                    activebackground="green", cursor="right_ptr", overrelief="sunken", command=root.quit)
    btn.place(x=180, y=20)

    btn.bind('<Enter>', on_enter_button)

    root.geometry("600x600+30+30")
    root.mainloop()
