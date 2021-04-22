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


class Setting(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('2000x1000')

    def comboexample(self):
        labeltop = tk.Label(self, text="Choose your favourite month")
        labeltop.grid(column=0, row=0)
        comboexample = ttk.Combobox(self, values=[
                                 "January",
                                 "February",
                                 "March",
                                 "April"])
        comboexample.grid(column=0, row=1)
        comboexample.current(1)
        self.mainloop()
