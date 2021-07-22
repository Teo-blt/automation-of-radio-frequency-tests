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
from Test_filter import Filter_script
import paramiko
from loguru import logger
from IHM import Graph_sensibility

# =============================================================================
THE_COLOR = "#E76145"

def filter_test_menu(self, ip_izepto, ip_ibts, port):
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
                                  command=lambda: [run(i_bts_entry.get(), i_zepto_entry.get())])
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

    make_a_graph_button = tk.Button(make_a_graph, text="Draw",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [Graph_sensibility.draw_graph()])
    make_a_graph_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

    add_climate_chamber = tk.Button(place, text="Add climate chamber",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [change()])
    add_climate_chamber.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    climate_chamber_label = Label(place, text="Select your climate chamber port com :")
    climate_chamber_entry = Entry(place)
    climate_chamber_entry.insert(0, port)
    def change():
        global number
        number = 1
        add_climate_chamber.forget(),
        climate_chamber_label.pack(padx=0, pady=10, expand=False,
                                   fill="none", side=TOP),
        climate_chamber_entry.pack(padx=0, pady=0, expand=False,
                                   fill="none", side=TOP)


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


def run(ip_ibts, ip_izepto):
    global launch_safety
    if launch_safety == 1:
        logger.critical("Error, the programme is already running")
    else:
        launch_safety = 1
        if func_izepto(ip_izepto) == 0:
            if func_ibts(ip_ibts) == 0:
                # self.destroy()
                Filter_script.Threadfilter(ip_izepto, ip_ibts).start()
        else:
            logger.warning("Please check your data")
