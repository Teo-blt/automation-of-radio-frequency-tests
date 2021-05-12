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
from tkinter.colorchooser import askcolor
from loguru import logger
# import Data_management as da
import Graphic
import sys
import serial

# ============================================================================
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        global the_color  # Creation of a global variable for the color of the buttons
        the_color = "#E76145"
        self.create_widgets()
        self.title("Main menu")
        self.withdraw()
        self.port = 'COM11'

    def create_widgets(self):  # Creation of a lobby menu
        new_window = tk.Toplevel(self)  # Setting of the new window
        new_window.configure(bg="grey")
        new_window.title("Start menu")
        new_window.geometry('700x200')
        label = tk.Label(new_window, text="Menu", )
        label.pack(padx=10, pady=10, expand=True, fill="both", side=TOP)
        button1 = tk.Button(new_window, text="Start",
                            borderwidth=8, background=the_color,  # To start the program, creation of a new window
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [self.combo("--choose your instrument here--"),
                                             self.deiconify(), new_window.withdraw()])
        button1.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button2 = tk.Button(new_window, text="Quit",
                            borderwidth=8, background=the_color,  # To quit the program
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [sys.exit()])
        button2.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button_settings = tk.Button(new_window, text="color", overrelief="sunken", bitmap="info", cursor="right_ptr",
                                    command=lambda: (self.color_change(new_window)))  # To change the color
        # of all buttons
        button_settings.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)

    def color_change(self, new_window):  # A very simple and mostly useless function to change the
        # color of all the buttons
        color = askcolor()  # wheel of color
        global the_color
        the_color = color[1]
        new_window.destroy()
        self.create_widgets()

    def combo(self, value):  # creation of a combobox, this combobox allow he user to chose a measuring tool in a list
        my_combo_frame = LabelFrame(self, text="Choice of instrument")
        my_combo_frame.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        label_example = tk.Label(my_combo_frame, text="Settings", font="arial", fg="black")
        label_example.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        label_top = tk.Label(my_combo_frame, text="Choose your measuring tool")
        label_top.pack(expand=False, fill="none", side=TOP)
        combo_example = ttk.Combobox(my_combo_frame, values=[
            "Climatic chamber",
            "Low frequency generator",  # The list of measuring tool
            "Signal generator",
            "Oscilloscope"], state="readonly")
        combo_example.set(value)
        combo_example.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
        button3 = tk.Button(my_combo_frame, text="validate",  # Button to validate a choice and launch the
                            # interface function
                            borderwidth=8, background=the_color,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken",
                            command=lambda: [self.interface(combo_example.current())])
        button3.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def interface(self, choice):  # This function open other functions after the choice of the user
        if choice == -1:
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            self.clear("Climatic chamber")  # Call the clear function to clean all the window
            self.climatic_chamber()  # Open Climatic chamber
        elif choice == 1:
            self.clear("Low frequency generator")  # Call the clear function to clean all the window
            self.lfg()  # Open frequency generator
        elif choice == 2:
            self.clear("Signal generator")  # Call the clear function to clean all the window
            self.sg()  # Open generator
        else:
            self.clear("Oscilloscope")  # Call the clear function to clean all the window
            self.osl()  # Open Oscilloscope

    def clear(self, get_title):  # Clear function, destroy all the window
        # and create a new window after the choice of the user
        self.destroy()
        Tk.__init__(self)
        self.title(get_title + " menu")
        self.combo(get_title)

    def climatic_chamber(self):  # The climatic chamber menu
        self.geometry("1200x500")  # Size of the window
        my_oven_frame = LabelFrame(self, text="Settings of the oven")
        my_oven_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        label2 = Label(my_oven_frame, text="Connection port :")
        label2.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        name = Entry(my_oven_frame)  # Function to collect the N° of the port of the measuring tool
        name.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        name.insert(0, self.port)
        button4 = Button(my_oven_frame, text="Connect", borderwidth=8, background=the_color,
                         activebackground="green", disabledforeground="grey",
                         cursor="right_ptr",
                         overrelief="sunken", command=lambda: [logger.info(f"The port [{name.get()}]"
                                                                           " was correctly selected"),
                                                               self.try_connect(name)])
        button4.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.scale()
        # Function not used
        # self.data_management()
        # self.save()
        return name.get()

    def try_connect(self, name):
        self.port = name.get()
        try:  # try to connect to the port com, 5 second of time out, this try allow me to use the program offline
            vt = serial.Serial(self.port, SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
            logger.debug("The connection was correctly established")
        except:
            logger.critical("Connection impossible")
            logger.critical("Please chek your connection port")
            logger.critical(f"Actual connection port: {self.port}")

    def scale(self):  # creation of two vey important buttons, Live draw example, a live draw (not used because
        # the user can easily break it), and Start the test, witch allow the user to enter in the management test area
        my_scale_frame = LabelFrame(self, text="Draw")
        my_scale_frame.grid(row=0, column=2, ipadx=0, ipady=0, padx=0, pady=0)
        button12 = tk.Button(my_scale_frame, text="Start the test",
                             borderwidth=8, background=the_color,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [Graphic.draw_5(self, the_color, self.climatic_chamber())])
        button12.pack(padx=10, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
        button11 = tk.Button(my_scale_frame, text="Live draw example",
                             borderwidth=8, background=the_color,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: Graphic.draw_4(self, the_color))
        button11.pack(padx=10, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=BOTTOM)

    def lfg(self):  # The low frequency generator menu
        self.geometry("1200x500")
        my_lfg_frame = LabelFrame(self, text="Settings of the Low frequency generator")
        my_lfg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)

    def sg(self):  # The signal generator menu
        self.geometry("1200x500")
        my_sg_frame = LabelFrame(self, text="Settings of the Signal generator")
        my_sg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)

    def osl(self):  # The oscilloscope menu
        self.geometry("1200x500")
        my_osl_frame = LabelFrame(self, text="Settings of the Oscilloscope")
        my_osl_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)

    """
    def data_management(self):
        my_data_management_frame = LabelFrame(self, text="Data_management")
        my_data_management_frame.grid(row=1, column=0, ipadx=40, ipady=5, padx=0, pady=0)
        label = tk.Label(my_data_management_frame, text="Data management Menu")
        label.pack()
        button6 = tk.Button(my_data_management_frame, text="Write what you want in the file",
                            borderwidth=8, background=the_color,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken",
                            command=lambda: da.write_file())
        button6.pack()
        button7 = tk.Button(my_data_management_frame, text="Read the file",
                            borderwidth=8, background=the_color,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken", command=lambda: da.read_file())
        button7.pack()
        button5 = tk.Button(my_data_management_frame, text="Delete file",
                            borderwidth=8, background=the_color,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken", command=lambda: da.delete_file())
        button5.pack()

    def save(self):
        my_save_frame = LabelFrame(self, text="Save menu")
        my_save_frame.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        button9 = tk.Button(my_save_frame, text="Save",
                            borderwidth=8, background=the_color,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=my_save_frame.quit)
        button9.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

        button8 = tk.Button(my_save_frame, text="Quit",
                            borderwidth=8, background=the_color,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: (self.leaving()))
        button8.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def leaving(self):
        if askyesno('Warning', 'Are you sure you want to do exit ?'):
            if askyesno('Warning', 'your data is not saved, are you sure you want to continue'):
                self.quit()
    """


Application().mainloop()
