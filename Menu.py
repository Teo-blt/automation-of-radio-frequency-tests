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
# Personal Imports
import page1 as p1
# =============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.creer_widgets()

    def creer_widgets(self):
        label = tk.Label(self, text="Menu")
        label.pack()
        bouton1 = tk.Button(self, text="Start", command=lambda: p1.Setting().comboexample())
        bouton1.pack()
        bouton2 = tk.Button(self, text="Quit", command=self.quit)
        bouton2.pack()


if __name__ == "__main__":
    app = Application()
    app.title("Application for the automation of radiofrequency tests ")
    app.mainloop()
