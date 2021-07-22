#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 17 12:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import tkinter as tk
from tkinter import *
from Test_sensibility import Sensibility_script
import paramiko
import time
from loguru import logger
import serial
from IHM import Graph_sensibility

# =============================================================================
THE_COLOR = "#E76145"


def sensibility_test_menu(self, port, ip_ibts, ip_izepto):
    global number
    number = 0
    scanner_ibts_frame = LabelFrame(self, text="Sensibility Menu")
    scanner_ibts_frame.grid(row=0, column=1, ipadx=10, ipady=10, padx=0, pady=0)
    ibts_scale_frame = LabelFrame(self, text="Start the test")
    ibts_scale_frame.grid(row=0, column=3, ipadx=0, ipady=0, padx=0, pady=0)
    make_a_graph = LabelFrame(self, text="Make a graph")
    make_a_graph.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    start_test_button = tk.Button(ibts_scale_frame, text="Ignition of the card",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [run(i_bts_entry.get(), i_zepto_entry.get(),
                                                       climate_chamber_entry.get(), self, number)])
    start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    place = scanner_ibts_frame

    i_bts_label = Label(place, text="Transmitter IP address:")
    i_bts_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    i_bts_entry = Entry(place)
    i_bts_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    i_bts_entry.insert(0, ip_ibts)

    i_zepto_label = Label(place, text="Receiver IP address:")
    i_zepto_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    i_zepto_entry = Entry(place)
    i_zepto_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    i_zepto_entry.insert(0, ip_izepto)

    add_climate_chamber = tk.Button(place, text="Add climate chamber",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [change()])
    add_climate_chamber.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

    climate_chamber_label = Label(place, text="Select your climate chamber port com :")
    climate_chamber_entry = Entry(place)
    climate_chamber_entry.insert(0, port)

    make_a_graph_button = tk.Button(make_a_graph, text="Draw",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [Graph_sensibility.draw_graph()])
    make_a_graph_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

    def change():
        global number
        number = 1
        add_climate_chamber.forget(),
        climate_chamber_label.pack(padx=0, pady=10, expand=False,
                                   fill="none", side=TOP),
        climate_chamber_entry.pack(padx=0, pady=0, expand=False,
                                   fill="none", side=TOP)


def func_ibts(ip_ibts):
    # ip_ibts = "192.168.4.228"
    try:
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_ibts, username=username, password=password)
        logger.info(f"Successfully connected to {ip_ibts}")
        return 0
    except:
        logger.critical(f"Impossible to connected to {ip_ibts}")


def func_izepto(ip_izepto):
    # ip_izepto = "192.168.120.1"
    try:
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip_izepto, username=username, password=password)
        logger.info(f"Successfully connected to {ip_izepto}")
        return 0
    except:
        logger.critical(f"Impossible to connected to {ip_izepto}")


def func_climate_chamber(port_test):
    # port_test = "COM11"
    try:
        wah = serial.Serial(port_test, 9600, timeout=5, writeTimeout=5)
        wah.write(b"$00I\n\r")
        time.sleep(0.2)
        received_frame = wah.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic chamber
        word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
        strings = str(word[1])
        number = float(strings)
        logger.info(f"Successfully connected to {port_test}")
        return 0
    except:
        logger.critical(f"Impossible to connected to {port_test}")


def three_methods_run_together(ip_ibts, ip_izepto, port_test, self):
    if func_ibts(ip_ibts) == 0:
        func_izepto(ip_izepto)
    if func_izepto(ip_izepto) == 0:
        func_climate_chamber(port_test)
    if func_climate_chamber(port_test) == 0:
        #self.destroy()
        Sensibility_script.Threadsensibility(ip_ibts, ip_izepto, port_test, self).start()
    else:
        logger.warning("Please check your data")


def two_methods_run_together(ip_ibts, ip_izepto, self):
    if func_ibts(ip_ibts) == 0:
        func_izepto(ip_izepto)
    if func_izepto(ip_izepto) == 0:
        #self.destroy()
        Sensibility_script.Threadsensibility(ip_ibts, ip_izepto, -1, self).start()
    else:
        logger.warning("Please check your data")


def run(ip_ibts, ip_izepto, port_test, self, number):
    global launch_safety
    if launch_safety == 1:
        logger.critical("Error, the programme is already running")
    else:
        launch_safety = 1
        if number:
            three_methods_run_together(ip_ibts, ip_izepto, port_test, self)
        else:
            two_methods_run_together(ip_ibts, ip_izepto, self)
