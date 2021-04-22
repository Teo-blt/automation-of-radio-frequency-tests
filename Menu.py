#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 18 16:00:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
# Personal Imports
# =============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.creer_widgets()
        self.withdraw()


    def combo(self):
        labelExample = tk.Label(self, text="Settings", fg="blue")
        labelExample.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        labeltop = tk.Label(self, text="Choose your measuring tool")
        labeltop.pack(expand=False, fill="none", side=TOP)
        comboexample = ttk.Combobox(self, values=[
                                     "Oven",
                                     "low frequency generator",
                                     "Signal generator",
                                     "Oscilloscope"],
                                state="readonly",)
        comboexample.pack(padx=5, pady=5, expand=False, fill="none", side=TOP)

    def creer_widgets(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("UwU")
        newWindow.geometry('100x100')
        label = tk.Label(newWindow, text="Menu")
        label.pack()
        bouton1 = tk.Button(newWindow, text="Start",command=lambda: [self.combo(), self.deiconify(), newWindow.withdraw()])
        bouton1.pack()
        bouton2 = tk.Button(newWindow, text="Quit", command=newWindow.destroy)
        bouton2.pack()

"""
if __name__ == "__main__":
    app = Application()
    app.title("Application for the automation of radiofrequency tests")
    app.mainloop()
"""
Application().mainloop()

