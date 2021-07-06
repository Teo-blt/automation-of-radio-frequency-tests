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
from loguru import logger
import serial
import pyvisa as visa

# =============================================================================
THE_COLOR = "#E76145"
global status
global version


def visual_function(visual_color_button, s):
    if s == 1:
        visual_color_button.config(text="The connection status is : offline", bg="red")
    else:
        visual_color_button.config(text="The connection status is : online", bg="light green")


def sg_menu(self, self_port):
    global status
    a = IntVar()
    scanner_gpib_frame = LabelFrame(self, text="Detection of GPIB")
    scanner_gpib_frame.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    place = scanner_gpib_frame
    radiobutton_frame = LabelFrame(scanner_gpib_frame)
    radiobutton_frame.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    Manual_connection = LabelFrame(self, text="Manual connection")
    Manual_connection.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)
    start_test_button = tk.Button(Manual_connection, text="Begin transmission",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [manual_launch(gpib_entry.get(), com_entry.get())])
    start_test_button.pack(padx=0, pady=0, ipadx=10, ipady=10, expand=False, fill="none", side=TOP)
    Manual_connection_gpib_label = Label(Manual_connection, text="GPIB address")
    Manual_connection_gpib_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    gpib_entry = Entry(Manual_connection)
    gpib_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    radiobutton_smiq_old = tk.Radiobutton(radiobutton_frame, text="GPIB USB",
                                          variable=a, value=0, cursor="right_ptr",
                                          indicatoron=0, command=lambda: [change_version(a.get()),
                                                                          com_entry.forget(),
                                                                          Manual_connection_port_label.forget()],
                                          background=THE_COLOR,
                                          activebackground="green",
                                          bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_smiq_old.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    radiobutton_smiq_new = tk.Radiobutton(radiobutton_frame, text="GPIB USB-C",
                                          variable=a, value=1, cursor="right_ptr",
                                          indicatoron=0, command=lambda: [change_version(a.get()),
                                                                          Manual_connection_port_label.pack(padx=0,
                                                                        pady=0, expand=False, fill="none", side=TOP), com_entry.pack(padx=0, pady=0, expand=False,
                                                                                         fill="none", side=TOP)],
                                          background=THE_COLOR,
                                          activebackground="green",
                                          bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_smiq_new.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    Manual_connection_port_label = Label(Manual_connection, text="Port COM")
    com_entry = Entry(Manual_connection)
    com_entry.insert(0, self_port)
    radiobutton_smiq_new.select()
    radiobutton_smiq_new.invoke()




def change_version(a):
    global version
    version = a


def manual_launch(gpib, port):
    global status
    global version
    port_com1 = "COM" + str(port)
    if version:
        try:
            ser = serial.Serial(port_com1, 9600, timeout=0.5)
            ser.write(('++addr ' + gpib + '\n').encode())
            ser.write("*IDN?\r".encode())
            ans = ser.readlines(ser.write(('++read\n'.encode())))
            word = ans[0]
            logger.debug(f"The connection was correctly established")
        except:
            logger.critical(f"The port [{port_com1}] or the GPIB {gpib} is not connected")
    else:
        try:
            rm = visa.ResourceManager()
            smiq_send = rm.open_resource("GPIB0" + '::' + port_com1 + '::INSTR')
            smiq_send.write('*RST')
            status = 1
            logger.debug("The connection was correctly established")
        except:
            logger.critical(f"The GPIB {port} is not connected")
