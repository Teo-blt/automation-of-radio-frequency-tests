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


def visual_function(visual_color_button, s):
    if s == 1:
        visual_color_button.config(text="The connection status is : offline", bg="red")
    else:
        visual_color_button.config(text="The connection status is : online", bg="light green")


def sg_menu(self, gpib_port):
    global status
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
    button_frame = LabelFrame(place, bd=0)  # , text="Scales"
    button_frame.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_button = Button(place, text="Scan", borderwidth=8, background=THE_COLOR,
                                           activebackground="green", disabledforeground="grey",
                                           cursor="right_ptr",
                                           overrelief="sunken",
                                           command=lambda: [write_gpib_scan(combobox_scan)])
    scanner_port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="The currently selected GPIB :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_entry = Label(place, text=gpib_port)
    port_com_frame_entry.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="Connection status :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    visual_color_button_sg = Button(place, state="disabled", disabledforeground="black")
    visual_color_button_sg.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    try:
        rm = visa.ResourceManager()
        smiq_send = rm.open_resource("GPIB1" + '::' + gpib_port + '::INSTR')
        smiq_send.write('*RST')
        status = 1
        visual_function(visual_color_button_sg, 0)
        logger.debug("The connection was correctly established")
    except:
        visual_function(visual_color_button_sg, 1)
        status = 0
    port_com_frame_label = Label(place, text="Connection port :")
    port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    combobox_scan = ttk.Combobox(place,
                                 values=[0], state="readonly")
    combobox_scan.set("--choose your port here--")
    combobox_scan.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)

    def automatic_1(e):
        return automatic(port_com_frame_entry, combobox_scan)

    def automatic(port_com_frame_entry, combobox_scan):
        change_combo_gpib(port_com_frame_entry, combobox_scan)
        change_gpib(combobox_scan, visual_color_button_sg)

    combobox_scan.bind("<<ComboboxSelected>>", automatic_1)
    write_gpib_scan(combobox_scan)


def call_graph_smiq(gpib_port):
    global type_gpib
    global status
    if status == 0:
        if askyesno("Warning", "The connection status is : offline\n Do you still want to continue ?"):
            test_SMIQ.lunch_smiq(gpib_port)
        else:
            pass
    else:
        test_SMIQ.lunch_smiq(gpib_port)

def write_gpib_scan(combobox_scan):
    global type_gpib
    [limit, multi_port] = scan_all_gpib()
    data = {}
    for i in range(0, limit):
        data[i] = str(multi_port[i])
    values = list(data.values())
    combobox_scan["values"] = values


def change_combo_gpib(port_com_frame_entry, combobox_scan):
    gpib_port = combobox_scan.get()
    port_com_frame_entry.config(text=gpib_port)


def change_gpib(combobox_scan, visual_color_button_sg):
    global status
    gpib_port = combobox_scan.get()
    try:
        rm = visa.ResourceManager()
        smiq_send = rm.open_resource("GPIB1" + '::' + gpib_port + '::INSTR')
        smiq_send.write('*RST')
        visual_function(visual_color_button_sg, 0)
        status = 1
        logger.debug("The connection was correctly established")
    except serial.serialutil.SerialException:
        logger.critical(f"The port [{gpib_port}] is not link to the climate chamber")
    except:
        logger.critical("Error unknown")
