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
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from loguru import logger
import Graphic
import serial
from Coroutines_experiment.devices_helper import scan_all_ports
from IHM_redirect import Menu_IBTS
from IHM_redirect import Menu_SMIQ
# ============================================================================


ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
LOBBY_WINDOW_SIZE = "700x200"
WINDOW_SIZE = "1200x500"
THE_COLOR = "#E76145"


def write_climate_chamber_scan(combobox_scan):
    [limit, multi_port] = scan_all_ports()
    data = {}
    for i in range(0, limit):
        data[i] = ("COM" + str(multi_port[i]))
    values = list(data.values())
    combobox_scan["values"] = values


def visual_function(visual_color_button, status):
    if status == 1:
        visual_color_button.config(text="The connection status is : offline")
        visual_color_button.config(bg="red", disabledforeground="black")
    else:
        visual_color_button.config(text="The connection status is : online")
        visual_color_button.config(bg="light green", disabledforeground="black")


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self._port = 'COM11'
        self._gpib_port = "25"
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

    def climatic_chamber_widget(self):
        self.geometry(WINDOW_SIZE)  # set window size
        scanner_port_com_frame = LabelFrame(self, text="Detection of port com")
        scanner_port_com_frame.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
        scanner_port_com_frame_label = Label(scanner_port_com_frame, text="Scanner for connection port")
        scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.scanner_button_climatic_chamber(scanner_port_com_frame)
        self.scale_climatic_chamber()
        # Function not used
        # self.data_management()
        # self.save()

    def scanner_button_climatic_chamber(self, place):
        scanner_port_com_frame_button = Button(place, text="Scan", borderwidth=8, background=THE_COLOR,
                                               activebackground="green", disabledforeground="grey",
                                               cursor="right_ptr",
                                               overrelief="sunken",
                                               command=lambda: [self.combobox_scan(port_com_frame_entry),
                                                                self.try_climate_chamber()])
        scanner_port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        scanner_port_com_frame_label = Label(place, text="The currently selected port :")
        scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        port_com_frame_entry = Label(place, text=self._port)
        port_com_frame_entry.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        scanner_port_com_frame_label = Label(place, text="Connection status :")
        scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.visual_color_button = Button(place, state="disabled")
        self.visual_color_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.try_climate_chamber()

    def try_climate_chamber(self, ):
        try:
            a = serial.Serial(self._port, SERIAL_SPEED, timeout=SERIAL_TIMEOUT, writeTimeout=WRITE_TIMEOUT)
            a.write(b"$00I\n\r")
            time.sleep(0.2)
            received_frame = a.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic chamber
            word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
            strings = str(word[1])
            number = float(strings)
            logger.info(f"The actual temperature of the climatic chamber is : {number}")
            self.status = 1
            visual_function(self.visual_color_button, 0)
        except:
            visual_function(self.visual_color_button, 1)

    def combobox_scan(self, port_com_frame_entry):
        port_com_frame = LabelFrame(self, text="Settings of the port com")
        port_com_frame.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        port_com_frame_label = Label(port_com_frame, text="Connection port :")
        port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.combobox_scanner = ttk.Combobox(port_com_frame, values=[0], state="readonly")
        self.combobox_scanner.set("--choose your port here--")
        self.combobox_scanner.pack(ipadx=0, ipady=0, padx=20, pady=10, expand=False, fill="x", side=TOP)
        write_climate_chamber_scan(self.combobox_scanner)
        port_com_frame_button = Button(port_com_frame, text="Connect", borderwidth=8, background=THE_COLOR,
                                       activebackground="green", disabledforeground="grey",
                                       cursor="right_ptr",
                                       overrelief="sunken",
                                       command=lambda: [
                                           self.climate_chamber_scan_validate(),
                                           self.change_combo_com(port_com_frame_entry)])
        port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

    def change_combo_com(self, port_com_frame_entry):
        port_com_frame_entry.config(text=self._port)

    def climate_chamber_scan_validate(self):
        if self.combobox_scanner.current() == -1:
            showerror("Error", "You must select a valid port")
        else:
            logger.info(f"The port [{self.combobox_scanner.get()}] was correctly selected"),
            self.change_port()

    def change_port(self):
        try:
            self._port = self.combobox_scanner.get()
            self.connection_test()
        except serial.serialutil.SerialException:
            logger.critical(f"The port [{self._port}] is not link to the climate chamber")
            self.status = 0
            visual_function(self.visual_color_button, 1)
        except:
            logger.critical("Error unknown")

    def connection_test(self):
        a = serial.Serial(self._port, SERIAL_SPEED, timeout=SERIAL_TIMEOUT, writeTimeout=WRITE_TIMEOUT)
        a.write(CLIMATIC_CHAMBER_STOP)
        visual_function(self.visual_color_button, 0)
        self.status = 1
        logger.debug("The connection was correctly established")

    def scale_climatic_chamber(self):  # creation of two vey important buttons, Live draw example,
        # a live draw (not used because the user can easily break it),
        # and Start the test, witch allow the user to enter in the management test area
        climatic_chamber_scale_frame = LabelFrame(self, text="Start the test")
        climatic_chamber_scale_frame.grid(row=0, column=3, ipadx=0, ipady=0, padx=0, pady=0)

        start_test_button = tk.Button(climatic_chamber_scale_frame, text="Start",
                                      borderwidth=8, background=THE_COLOR,
                                      activebackground="green", cursor="right_ptr", overrelief="sunken",
                                      command=lambda:
                                      [self.call_graph_climatic_chamber()])
        start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

    def call_graph_climatic_chamber(self):
        try:
            self.connection_test()
        except:
            self.status = 0
            visual_function(self.visual_color_button, 1)
        if self.status == 0:
            if askyesno("Warning", "The connection status is : offline\n Do you still want to continue ?"):
                Graphic.main_graphic_climatic_chamber(self, self._port)
            else:
                pass
        else:
            Graphic.main_graphic_climatic_chamber(self, self._port)

    def sg(self):  # The signal generator menu
        self.geometry(WINDOW_SIZE)
        Menu_SMIQ.sg_menu(self, self.type_gpib, self._gpib_port)
    def ibts(self):
        self.geometry(WINDOW_SIZE)
        Menu_IBTS.ibts_menu(self, self._ip_adress)


Application().mainloop()
