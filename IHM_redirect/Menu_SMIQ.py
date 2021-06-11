#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 11 14:16:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from loguru import logger
import serial
from SMIQ import test_SMIQ
import pyvisa as visa
from Coroutines_experiment.devices_helper import scan_all_gpib

# =============================================================================
THE_COLOR = "#E76145"
global status
global type_gpib


def visual_function(visual_color_button, s):
    if s == 1:
        visual_color_button.config(text="The connection status is : offline")
        visual_color_button.config(bg="red", disabledforeground="black")
    else:
        visual_color_button.config(text="The connection status is : online")
        visual_color_button.config(bg="light green", disabledforeground="black")


def sg_menu(self, type_gpib_give, gpib_port):
    global type_gpib
    global status
    type_gpib = type_gpib_give
    a = IntVar()
    scanner_gpib_frame = LabelFrame(self, text="Detection of GPIB")
    scanner_gpib_frame.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    gpib_scale_frame = LabelFrame(self, text="Start the test")
    gpib_scale_frame.grid(row=0, column=3, ipadx=0, ipady=0, padx=0, pady=0)
    start_test_button = tk.Button(gpib_scale_frame, text="Begin transmission",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [call_graph_smiq(gpib_port)])
    start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    place = scanner_gpib_frame
    scanner_port_com_frame_label = Label(place, text="The currently type of connection :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    button_frame = LabelFrame(place, bd=0)  # , text="Scales"
    button_frame.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    radiobutton_gpib = tk.Radiobutton(button_frame, text="GPIB/GPIB",
                                      variable=a, value=0, cursor="right_ptr",
                                      indicatoron=0, command=lambda: [change_type(str(a.get()))],
                                      background=THE_COLOR,
                                      activebackground="green",
                                      bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_gpib.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    radiobutton_gpib.invoke()
    radiobutton_gpib_usb = tk.Radiobutton(button_frame, text="GPIB/USB",
                                          variable=a, value=1, cursor="right_ptr",
                                          indicatoron=0, command=lambda: [change_type(str(a.get()))],
                                          background=THE_COLOR,
                                          activebackground="green",
                                          bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_gpib_usb.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scanner_port_com_frame_button = Button(place, text="Scan", borderwidth=8, background=THE_COLOR,
                                           activebackground="green", disabledforeground="grey",
                                           cursor="right_ptr",
                                           overrelief="sunken",
                                           command=lambda: [gpib_scan(self, port_com_frame_entry)])
    scanner_port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="The currently selected GPIB :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_entry = Label(place, text=gpib_port)
    port_com_frame_entry.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="Connection status :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    visual_color_button_sg = Button(place, state="disabled")
    visual_color_button_sg.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    try:
        rm = visa.ResourceManager()
        smiq_send = rm.open_resource(self.type_gpib + '::' + self._gpib_port + '::INSTR')
        smiq_send.write('*RST')
        status = 1
        visual_function(visual_color_button_sg, 0)
    except:
        visual_function(visual_color_button_sg, 1)
        status = 0

def call_graph_smiq(gpib_port):
    global type_gpib
    global status
    if status == 0:
        if askyesno("Warning", "The connection status is : offline\n Do you still want to continue ?"):
            test_SMIQ.lunch_smiq(gpib_port, type_gpib)
        else:
            pass
    else:
        test_SMIQ.lunch_smiq(gpib_port, type_gpib)


def change_type(type):
    global type_gpib
    type_gpib = "GPIB" + type


def gpib_scan(self, port_com_frame_entry):
    port_com_frame = LabelFrame(self, text="Settings of the GPIB")
    port_com_frame.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
    port_com_frame_label = Label(port_com_frame, text="Connection port :")
    port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    combobox_scan = ttk.Combobox(port_com_frame,
                                 values=[0], state="readonly")
    combobox_scan.set("--choose your port here--")
    combobox_scan.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
    write_gpib_scan(combobox_scan)
    port_com_frame_button = Button(port_com_frame, text="Connect", borderwidth=8, background=THE_COLOR,
                                   activebackground="green", disabledforeground="grey",
                                   cursor="right_ptr",
                                   overrelief="sunken",
                                   command=lambda: [self.gpib_scan_validate(combobox_scan),
                                                    self.change_combo_gpib(port_com_frame_entry)])
    port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)


def write_gpib_scan(combobox_scan):
    global type_gpib
    [limit, multi_port] = scan_all_gpib(type_gpib)
    data = {}
    for i in range(0, limit):
        data[i] = str(multi_port[i])
    values = list(data.values())
    combobox_scan["values"] = values


def change_combo_gpib(port_com_frame_entry, gpib_port):
    port_com_frame_entry.config(text=gpib_port)


def change_gpib(name, visual_color_button_sg):
    global type_gpib
    global status
    gpib_port = name
    try:
        rm = visa.ResourceManager()
        smiq_send = rm.open_resource(type_gpib + '::' + gpib_port + '::INSTR')
        smiq_send.write('*RST')
        visual_function(visual_color_button_sg, 0)
        status = 1
        logger.debug("The connection was correctly established")
    except serial.serialutil.SerialException:
        logger.critical(f"The port [{gpib_port}] is not link to the climate chamber")
    except:
        logger.critical("Error unknown")
