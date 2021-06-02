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


# =============================================================================
def sequencer(self):
    sequencer_frame = LabelFrame(self)
    sequencer_frame.grid(row=0, column=2, ipadx=40, ipady=40, padx=0, pady=0, rowspan=4)
    sequencer_label = tk.Label(sequencer_frame, text="Sequencer frame", bg="white", font="arial",
                               fg="black", relief="groove")
    sequencer_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    sequencer_label_2 = tk.Label(sequencer_frame, text="in progress...")
    sequencer_label_2.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
