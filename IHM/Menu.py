#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 23 16:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from IHM_redirect import Menu_IBTS
from IHM_redirect import Menu_SMIQ
from IHM_redirect import Menu_Climatic_chamber

# ============================================================================

LOBBY_WINDOW_SIZE = "700x200"
WINDOW_SIZE = "1200x500"
THE_COLOR = "#E76145"

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self._port = 'COM11'
        self._gpib_port = "24"
        self._ip_adress = "192.168.4.228"
        self.status = 0
        self.interface(0)
        self.type_gpib = "GPIB0"

    def setting_lobby_window(self) -> Toplevel:
        new_window = tk.Toplevel(self)
        new_window.configure(bg="grey")
        new_window.title("Start menu")
        new_window.geometry(LOBBY_WINDOW_SIZE)
        return new_window

    def create_choose_measuring_tool_combobox(self, value: str):
        """
        creation of a combobox, this combobox allow user to choose a measuring tool in a list
        :param value: value of the combobox
        """
        instrument_choose_combobox = LabelFrame(self, text="Choice of instrument")
        instrument_choose_combobox.grid(row=0, column=0, ipadx=40, ipady=20, padx=0, pady=0)

        settings_label = tk.Label(instrument_choose_combobox, text="Settings", font="arial", fg="black")
        settings_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

        label_top = tk.Label(instrument_choose_combobox, text="Choose your measuring tool")
        label_top.pack(expand=False, fill="none", side=TOP)

        choose_measuring_tool_combobox = ttk.Combobox(instrument_choose_combobox, values=[
            "Climatic chamber",  # The list of measuring tool
            "Signal generator",
            "IBTS"], state="readonly")

        def chose(e, i=choose_measuring_tool_combobox):
            return validate(e, i)

        def validate(e, choose_measuring_tool_combobox):
            self.interface(choose_measuring_tool_combobox.current())

        choose_measuring_tool_combobox.bind("<<ComboboxSelected>>", chose)
        choose_measuring_tool_combobox.set(value)
        choose_measuring_tool_combobox.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)

    def interface(self, choice):  # This function open other functions after the choice of the user
        if choice == -1:
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            self.create_new_window("Climatic chamber")  # Call the clear function to clean all the window
            self.climatic_chamber_widget()  # Open Climatic chamber
        elif choice == 1:
            self.create_new_window("Signal generator")  # Call the clear function to clean all the window
            self.sg()  # Open generator
        elif choice == 2:
            self.create_new_window("IBTS")  # Call the clear function to clean all the window
            self.ibts()  # Open generator

    def create_new_window(self, window_title: str):
        """
        Clear function, destroy all the windows and create a new window after the choice of the user
        :param window_title:
        """
        self.destroy()
        Tk.__init__(self)
        self.title(window_title + " menu")
        self.create_choose_measuring_tool_combobox(window_title)
        #  Sequencer.sequencer(self) not use anymore



    def sg(self):  # The signal generator menu
        self.geometry(WINDOW_SIZE)
        Menu_SMIQ.sg_menu(self, self.type_gpib, self._gpib_port)

    def ibts(self):  # The IBTS menu
        self.geometry(WINDOW_SIZE)
        Menu_IBTS.ibts_menu(self, self._ip_adress)

    def climatic_chamber_widget(self):  # The climatic_chamber menu
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_Climatic_chamber.start_climatic_chamber(self, self._port)

Application().mainloop()
