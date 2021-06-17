#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 11 14:16:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from loguru import logger
from IHM import Graphic
import serial
from Coroutines_experiment.devices_helper import scan_all_ports

# =============================================================================
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
THE_COLOR = "#E76145"
global status


def start_climatic_chamber(self, port_give):
    global port
    port = port_give
    scanner_port_com_frame = LabelFrame(self, text="Detection of port com")
    scanner_port_com_frame.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    scanner_port_com_frame_label = Label(scanner_port_com_frame, text="Scanner for connection port")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    place = scanner_port_com_frame
    scanner_port_com_frame_button = Button(place, text="Scan", borderwidth=8, background=THE_COLOR,
                                           activebackground="green", disabledforeground="grey",
                                           cursor="right_ptr",
                                           overrelief="sunken",
                                           command=lambda: [write_climate_chamber_scan(combobox_scanner),
                                                            try_climate_chamber(port, visual_color_button)])
    scanner_port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="The currently selected port :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_entry = Label(place, text=port)
    port_com_frame_entry.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="Connection status :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    visual_color_button = Button(place, state="disabled", disabledforeground="black")
    visual_color_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_label = Label(place, text="Connection port :")
    port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    combobox_scanner = ttk.Combobox(place, values=[0], state="readonly")
    combobox_scanner.set("--choose your port here--")
    combobox_scanner.pack(ipadx=0, ipady=0, padx=20, pady=10, expand=False, fill="x", side=TOP)

    def automatic_1(e):
        return automatic(combobox_scanner, visual_color_button, port_com_frame_entry)

    def automatic(combobox_scanner, visual_color_button, port_com_frame_entry):
        climate_chamber_scan_validate(combobox_scanner, visual_color_button),
        change_combo_com(port_com_frame_entry, combobox_scanner)

    combobox_scanner.bind("<<ComboboxSelected>>", automatic_1)
    scale_climatic_chamber(self, visual_color_button)
    try_climate_chamber(port, visual_color_button)
    write_climate_chamber_scan(combobox_scanner)


def visual_function(visual_color_button, s):
    if s == 1:
        visual_color_button.config(text="The connection status is : offline", bg="red")
    else:
        visual_color_button.config(text="The connection status is : online", bg="light green")


def try_climate_chamber(port, visual_color_button):
    global status
    try:
        a = serial.Serial(port, SERIAL_SPEED, timeout=SERIAL_TIMEOUT, writeTimeout=WRITE_TIMEOUT)
        a.write(b"$00I\n\r")
        time.sleep(0.2)
        received_frame = a.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic chamber
        word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
        strings = str(word[1])
        number = float(strings)
        status = 1
        visual_function(visual_color_button, 0)
    except:
        status = 0
        visual_function(visual_color_button, 1)
        logger.critical(f"The port [{port}] is not link to the climate chamber")


def write_climate_chamber_scan(combobox_scan):
    [limit, multi_port] = scan_all_ports()
    data = {}
    for i in range(0, limit):
        data[i] = ("COM" + str(multi_port[i]))
    values = list(data.values())
    combobox_scan["values"] = values


def change_combo_com(port_com_frame_entry, combobox_scanner):
    global port
    port = combobox_scanner.get()
    port_com_frame_entry.config(text=port)


def climate_chamber_scan_validate(combobox_scanner, visual_color_button):
    if combobox_scanner.current() == -1:
        showerror("Error", "You must select a valid port")
    else:
        logger.info(f"The port [{combobox_scanner.get()}] was correctly selected"),
        change_port(combobox_scanner, visual_color_button)


def change_port(combobox_scanner, visual_color_button):
    global status
    try:
        port_test = combobox_scanner.get()
        a = serial.Serial(port_test, SERIAL_SPEED, timeout=SERIAL_TIMEOUT, writeTimeout=WRITE_TIMEOUT)
        a.write(b"$00I\n\r")
        time.sleep(0.2)
        received_frame = a.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic chamber
        word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
        strings = str(word[1])
        number = float(strings)
        logger.debug(f"The connection was correctly established")
        status = 1
        visual_function(visual_color_button, 0)
    except:
        logger.critical(f"The port [{port_test}] is not link to the climate chamber")
        status = 0
        visual_function(visual_color_button, 1)


def scale_climatic_chamber(self, visual_color_button):  # creation of two vey important buttons, Live draw example,
    # a live draw (not used because the user can easily break it),
    # and Start the test, witch allow the user to enter in the management test area
    climatic_chamber_scale_frame = LabelFrame(self, text="Start the test")
    climatic_chamber_scale_frame.grid(row=0, column=3, ipadx=0, ipady=0, padx=0, pady=0)

    start_test_button = tk.Button(climatic_chamber_scale_frame, text="Start",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda:
                                  [call_graph_climatic_chamber(self, visual_color_button)])
    start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)


def call_graph_climatic_chamber(self, visual_color_button):
    global port
    global status
    try_climate_chamber(port, visual_color_button)
    if status == 0:
        if askyesno("Warning", "The connection status is : offline\n Do you still want to continue ?"):
            Graphic.main_graphic_climatic_chamber(self, port)
        else:
            pass
    else:
        Graphic.main_graphic_climatic_chamber(self, port)
