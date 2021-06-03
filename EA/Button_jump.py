#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 2 14:30:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import tkinter as tk
import random


# =============================================================================

def play(e):
    def text_var():
        text = {}
        text[0] = "You good a this !"
        text[1] = "Nice try !"
        text[2] = "You doing great !"
        text[3] = "Keep going !"
        text[4] = "Almost done !"
        text[5] = "That was close  !"
        text[6] = "You got it !"
        text[7] = "You have it in your blood !"
        text[8] = "Enjoy the inexorable pain"
        text[9] = "Time is flying"
        text[10] = "No pain, no gain."
        text[11] = "Did you do this your all life ?"
        text[12] = "When are you stopping ?"
        text[13] = "Come on, we don't have all day"
        text[14] = "How could you miss that ?"
        text[15] = "Yare Yare Daze..."
        text[16] = "On you go !"
        text[17] = "That's better !"
        text[18] = "Not bad !"
        text[19] = "Yes, that's it !"
        text[20] = "You're nearly there !"
        text[21] = "Is that all you got ?"
        text[22] = "You're doing fine !"
        text[23] = "Don't give up !"
        text[24] = "Try again !"
        text[25] = "Try to do it again !"
        text[26] = "I'm sure it will be all right next time !"
        text[27] = "I'm sure you can do even better !"
        text[28] = "You see, it wasn't that difficult !"
        text[29] = "Click on the button to exit the application"
        i = random.randint(1, 29)
        return text[i]

    def on_enter_button(e):
        w = root.winfo_width()
        h = root.winfo_height()

        b_w = btn.winfo_width()
        b_h = btn.winfo_height()

        r_x = random.randrange(0, w - b_w)
        r_y = random.randrange(0, h - b_h)

        btn.place(x=r_x, y=r_y)
        label.config(text=text_var())

    root = tk.Tk()
    root.title('Jumping button')

    label = tk.Label(root, text="Click on the button to exit the application", bg="white",
                     font="arial", fg="black", relief="groove")
    label.pack(padx=1, pady=1, expand=True, fill="both")

    btn = tk.Button(root, text='Exit', width=10, borderwidth=8, background="#E76145",
                    activebackground="green", cursor="right_ptr", overrelief="sunken", command=root.quit)
    btn.place(x=180, y=20)
    btn.bind('<Enter>', on_enter_button)

    root.geometry("600x600+30+30")
    root.resizable(False, False)
    root.mainloop()
