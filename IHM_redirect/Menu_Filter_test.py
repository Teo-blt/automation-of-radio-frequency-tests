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
from IHM_piloting.Test_filter import Filter_script
import paramiko
from loguru import logger
from IHM import Graph_sensibility
import serial
import time
from tkinter import filedialog
import pandas as pd

# =============================================================================
THE_COLOR = "#E76145"
global launch_safety
launch_safety = 0


def filter_test_menu(self, ip_izepto, ip_ibts, port):
    global number
    number = 0
    scanner_ibts_frame = LabelFrame(self, text="Filter Menu")
    scanner_ibts_frame.grid(row=0, column=1, ipadx=10, ipady=10, padx=0, pady=0)
    ibts_scale_frame = LabelFrame(self, text="Start the test")
    ibts_scale_frame.grid(row=0, column=3, ipadx=0, ipady=0, padx=0, pady=0)
    make_a_graph = LabelFrame(self, text="Make a graph")
    make_a_graph.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    start_test_button = tk.Button(ibts_scale_frame, text="Ignition of the card",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [run(i_bts_entry.get(), i_zepto_entry.get(),
                                                       climate_chamber_entry.get(), number)])
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
                                    command=lambda: [Graph_sensibility.draw_graph(self)])
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


def three_methods_run_together(ip_ibts, ip_izepto, port_test, file_name):
    if func_ibts(ip_ibts) == 0:
        if func_izepto(ip_izepto) == 0:
            if func_climate_chamber(port_test) == 0:
                # self.destroy()
                Filter_script.Threadfilter(ip_izepto, ip_ibts, port_test, file_name).start()
    else:
        logger.warning("Please check your data")


def two_methods_run_together(ip_ibts, ip_izepto, file_name):
    if func_ibts(ip_ibts) == 0:
        if func_izepto(ip_izepto) == 0:
            # self.destroy()
            Filter_script.Threadfilter(ip_izepto, ip_ibts, -1, file_name).start()
    else:
        logger.warning("Please check your data")


def run(ip_ibts, ip_izepto, port_test, number):
    global launch_safety
    if launch_safety == 1:
        logger.critical("Error, the programme is already running")
    else:
        launch_safety = 1
        if number:
            three_methods_run_together(ip_ibts, ip_izepto, port_test, 0)
        else:
            two_methods_run_together(ip_ibts, ip_izepto, 0)
        #ask_order_file(ip_ibts, ip_izepto, port_test, number)


def ask_order_file(ip_ibts, ip_izepto, port_test, number):
    def uploadaction(file_entry):
        filename = filedialog.askopenfilename(filetypes=[("text files", ".txt")])
        file_entry.delete(0, 2000)
        file_entry.insert(0, filename)

    window_graph_data = Tk()
    menu_frame = LabelFrame(window_graph_data, text="Menu")
    menu_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    configuration_file = Entry(menu_frame, cursor="right_ptr")
    configuration_file.pack(expand=False, fill="none", side=TOP)
    configuration_file.insert(0, "Select command file")
    import_file_button = Button(menu_frame, text="Import file",
                                borderwidth=8, background=THE_COLOR,
                                activebackground="green", cursor="right_ptr", overrelief="sunken",
                                command=lambda: [uploadaction(configuration_file)])
    import_file_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    check_button = Button(menu_frame, text="Check file",
                          borderwidth=8, background=THE_COLOR,
                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                          command=lambda: [verification(ip_ibts, ip_izepto, port_test, number,
                                                        str(configuration_file.get()), window_graph_data)])
    check_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)


def verification(ip_ibts, ip_izepto, port_test, number, file_name, window_graph_data):
    try:
        data = pd.read_csv(file_name, sep='\s+', header=None)
        data = pd.DataFrame(data)
        a = file_name.split('/')
        if a[-1] == 'Orders.txt':
            window_graph_data.destroy()
            if number:
                three_methods_run_together(ip_ibts, ip_izepto, port_test, file_name)
            else:
                two_methods_run_together(ip_ibts, ip_izepto, file_name)
        else:
            logger.critical(f"The file is not 'Orders.txt'")
    except:
        logger.critical(f"The file name {file_name} is invalid")
