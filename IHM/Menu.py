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
import Graphic
import sys
import serial

# ============================================================================
from Coroutines_experiment.devices_helper import scan_all_ports

LOBBY_WINDOW_SIZE = "700x200"
WINDOW_SIZE = "1200x500"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 1


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        global the_color  # the color of the buttons
        the_color = "#E76145"
        self.setting_up_lobby_widget()
        self.title("Main menu")
        self.withdraw()
        self._port = 'COM11'

    def setting_up_lobby_widget(self):  # Creation of a lobby menu
        lobby_window: Toplevel = self.setting_lobby_window()

        label = tk.Label(lobby_window, text="Menu", )
        label.pack(padx=10, pady=10, expand=True, fill="both", side=TOP)

        self.setting_up_start_button(lobby_window)
        self.setting_up_quit_button(lobby_window)
        self.setting_up_setting_button(lobby_window)

    def setting_up_setting_button(self, lobby_window: Toplevel):
        button_settings = tk.Button(
            lobby_window, text="color", overrelief="sunken", bitmap="info", cursor="right_ptr",
            command=lambda: (self.color_change(lobby_window)))  # To change the color of all buttons
        button_settings.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)

    def setting_up_quit_button(self, lobby_window: Toplevel):
        quit_button = tk.Button(
            lobby_window,
            text="Quit",
            borderwidth=8,
            background=the_color,  # To quit the program
            activebackground="green",
            cursor="right_ptr",
            overrelief="sunken",
            command=lambda: [sys.exit()]
        )
        quit_button.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def setting_up_start_button(self, lobby_window: Toplevel):
        start_button = tk.Button(
            lobby_window,
            text="Start",
            borderwidth=8,
            background=the_color,  # To start the program, creation of a new window
            activebackground="green",
            cursor="right_ptr",
            overrelief="sunken",
            command=lambda: [
                self.create_choose_measuring_tool_combobox("--choose your instrument here--"),
                self.deiconify(), lobby_window.withdraw()])
        start_button.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def setting_lobby_window(self) -> Toplevel:
        new_window = tk.Toplevel(self)
        new_window.configure(bg="grey")
        new_window.title("Start menu")
        new_window.geometry(LOBBY_WINDOW_SIZE)

        return new_window

    def color_change(self, new_window):
        """
        A very simple and mostly useless function to change the color of all the buttons
        :param new_window:
        :return:
        """
        color = askcolor()  # wheel of color
        global the_color
        the_color = color[1]
        new_window.destroy()
        self.setting_up_lobby_widget()

    def create_choose_measuring_tool_combobox(self, value: str):
        """
        creation of a combobox, this combobox allow user to choose a measuring tool in a list
        :param value: value of the combobox
        """
        instrument_choose_combobox = LabelFrame(self, text="Choice of instrument")
        instrument_choose_combobox.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)

        settings_label = tk.Label(instrument_choose_combobox, text="Settings", font="arial", fg="black")
        settings_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

        label_top = tk.Label(instrument_choose_combobox, text="Choose your measuring tool")
        label_top.pack(expand=False, fill="none", side=TOP)

        choose_measuring_tool_combobox = ttk.Combobox(instrument_choose_combobox, values=[
            "Climatic chamber",
            "Low frequency generator",  # The list of measuring tool
            "Signal generator",
            "Oscilloscope"], state="readonly")
        choose_measuring_tool_combobox.set(value)
        choose_measuring_tool_combobox.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
        self.setting_up_validate_button(instrument_choose_combobox, choose_measuring_tool_combobox)

    def setting_up_validate_button(self, instrument_choose_combobox, choose_measuring_tool_combobox):
        validate_button = tk.Button(
            instrument_choose_combobox,
            text="validate",
            borderwidth=8,
            background=the_color,
            activebackground="green",
            disabledforeground="grey",
            cursor="right_ptr",
            overrelief="sunken",
            command=lambda: [self.interface(choose_measuring_tool_combobox.current())])
        validate_button.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def interface(self, choice):  # This function open other functions after the choice of the user
        if choice == -1:
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            self.create_new_window("Climatic chamber")  # Call the clear function to clean all the window
            self.climatic_chamber_widget()  # Open Climatic chamber
        elif choice == 1:
            self.create_new_window("Low frequency generator")  # Call the clear function to clean all the window
            self.low_frequency_generator_widget()  # Open frequency generator
        elif choice == 2:
            self.create_new_window("Signal generator")  # Call the clear function to clean all the window
            self.sg()  # Open generator
        else:
            self.create_new_window("Oscilloscope")  # Call the clear function to clean all the window
            self.osl()  # Open Oscilloscope

    def create_new_window(self, window_title: str):
        """
        Clear function, destroy all the windows and create a new window after the choice of the user
        :param window_title:
        """
        self.destroy()
        Tk.__init__(self)
        self.title(window_title + " menu")
        self.create_choose_measuring_tool_combobox(window_title)

    def climatic_chamber_widget(self):
        self.geometry(WINDOW_SIZE)  # set window size
        scanner_port_com_frame = LabelFrame(self, text="Detection of port com")
        scanner_port_com_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        scanner_port_com_frame_label = Label(scanner_port_com_frame, text="Scanner for connection port")
        scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.setting_up_scanner_button(scanner_port_com_frame)
        self.scale()
        # Function not used
        # self.data_management()
        # self.save()

    def setting_up_scanner_button(self, scanner_port_com_frame):
        scanner_port_com_frame_button = Button(scanner_port_com_frame, text="Scan", borderwidth=8, background=the_color,
                                               activebackground="green", disabledforeground="grey",
                                               cursor="right_ptr",
                                               overrelief="sunken",
                                               command=lambda: [self.combobox_scan()])
        scanner_port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        scanner_port_com_frame_label = Label(scanner_port_com_frame, text="The currently selected port :")
        scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        port_com_frame_entry = Entry(scanner_port_com_frame)
        port_com_frame_entry.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        port_com_frame_entry.insert(0, self._port)
    def combobox_scan(self):
        port_com_frame = LabelFrame(self, text="Settings of the port com")
        port_com_frame.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        port_com_frame_label = Label(port_com_frame, text="Connection port :")
        port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        combobox_scan = ttk.Combobox(port_com_frame,
                                     values=[self.write_combobox_scan()], state="readonly")
        combobox_scan.set("--choose your port here--")
        combobox_scan.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
        port_com_frame_button = Button(port_com_frame, text="Connect", borderwidth=8, background=the_color,
                                       activebackground="green", disabledforeground="grey",
                                       cursor="right_ptr",
                                       overrelief="sunken",
                                       command=lambda: [self.combobox_scan_validate(combobox_scan)])
        port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

    def write_combobox_scan(self):
        [limit, multi_port] = scan_all_ports(self._port)
        data = {}
        for i in range(0, limit):
            data[i] = ("COM" + str(multi_port[i]))
        values = list(data.values())
        print(values)
        return values

    def combobox_scan_validate(self, combobox_scan):
        if combobox_scan.current() == -1:
            showerror("Error", "You must select a valid port")
        else:
            logger.info(f"The port [{combobox_scan.get()}] was correctly selected"),
            self.change_port(combobox_scan.get())

    def change_port(self, name):
        self._port = name
        try:
            if self._port == "COM11":
                logger.critical("you're already trying to connect to this port")
            else:
                serial.Serial(self._port, SERIAL_SPEED, timeout=SERIAL_TIMEOUT).open()
                logger.debug("The connection was correctly established")
        except serial.serialutil.SerialException:
            logger.critical("This port does not exist")
        except:
            logger.critical("Error unknown")

    def scale(self):  # creation of two vey important buttons, Live draw example, a live draw (not used because
        # the user can easily break it), and Start the test, witch allow the user to enter in the management test area
        my_scale_frame = LabelFrame(self, text="Draw")
        my_scale_frame.grid(row=0, column=2, ipadx=0, ipady=0, padx=0, pady=0)

        start_test_button = tk.Button(my_scale_frame, text="Start the test",
                                      borderwidth=8, background=the_color,
                                      activebackground="green", cursor="right_ptr", overrelief="sunken",
                                      command=lambda:
                                      [Graphic.main_graphic_climatic_chamber(self, the_color,
                                                                             self.climatic_chamber_widget())])
        start_test_button.pack(padx=10, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
        """
        button11 = tk.Button(my_scale_frame, text="Live draw example",
                             borderwidth=8, background=the_color,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: Graphic.live_graph(self, the_color))
        button11.pack(padx=10, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=BOTTOM)
        """

    def low_frequency_generator_widget(self):
        self.geometry(WINDOW_SIZE)
        my_lfg_frame = LabelFrame(self, text="Settings of the Low frequency generator")
        my_lfg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)

    def sg(self):  # The signal generator menu
        self.geometry(WINDOW_SIZE)
        my_sg_frame = LabelFrame(self, text="Settings of the Signal generator")
        my_sg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)

    def osl(self):  # The oscilloscope menu
        self.geometry(WINDOW_SIZE)
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
