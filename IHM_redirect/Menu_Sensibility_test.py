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
global validation
validation = 0


def sensibility_test_menu(self, port, ip_address, carte_ip_address):
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
                                  command=lambda: [run(iBTS_entry.get(), iZepto_entry.get(),
                                                       climate_chamber_entry.get(), self, number)])
    start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    place = scanner_ibts_frame

    iBTS_label = Label(place, text="Select your iBTS IP address:")
    iBTS_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    iBTS_entry = Entry(place)
    iBTS_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    iBTS_entry.insert(0, ip_address)

    iZepto_label = Label(place, text="Select your iZepto IP address:")
    iZepto_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    iZepto_entry = Entry(place)
    iZepto_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    iZepto_entry.insert(0, carte_ip_address)

    climate_chamber_label = Label(place, text="Select your climate chamber port com :")
    climate_chamber_entry = Entry(place)
    climate_chamber_entry.insert(0, port)

    Add_climate_chamber = tk.Button(place, text="Add climate chamber",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [change()])
    Add_climate_chamber.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

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
        Add_climate_chamber.forget(),
        climate_chamber_label.pack(padx=0, pady=10, expand=False,
                                   fill="none", side=TOP),
        climate_chamber_entry.pack(padx=0, pady=0, expand=False,
                                   fill="none", side=TOP)


def func_a(ip_address):
    # ip_address = "192.168.4.228"
    global validation
    try:
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        logger.info(f"Successfully connected to {ip_address}")
        validation = validation + 1
        return ssh
    except:
        logger.critical(f"Impossible to connected to {ip_address}")


def func_b(ip):
    # ip = "192.168.120.1"
    global validation
    try:
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=ip, username=username, password=password)
        logger.info(f"Successfully connected to {ip}")
        validation = validation + 1
        return ssh2
    except:
        logger.critical(f"Impossible to connected to {ip}")


def func_c(port_test):
    # port_test = "COM11"
    global validation
    try:
        wah = serial.Serial(port_test, 9600, timeout=5, writeTimeout=5)
        wah.write(b"$00I\n\r")
        time.sleep(0.2)
        received_frame = wah.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic chamber
        word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
        strings = str(word[1])
        number = float(strings)
        logger.info(f"Successfully connected to {port_test}")
        validation = validation + 1
        return wah
    except:
        logger.critical(f"Impossible to connected to {port_test}")


def three_methods_run_together(ip_address, ip, port_test, self):
    global validation
    func_a(ip_address)
    func_b(ip)
    func_c(port_test)
    if validation == 3:
        # self.destroy()
        Sensibility_script.Thread_sensibility(ip_address, ip, port_test).run()
    else:
        logger.warning("Please check your data")


def two_methods_run_together(ip_address, ip, self):
    global validation
    func_a(ip_address)
    func_b(ip)
    if validation == 2:
        #self.destroy()
        Sensibility_script.Thread_sensibility(ip_address, ip, -1).run()
    else:
        logger.warning("Please check your data")


def run(ip_address, ip, port_test, self, number):
    if number:
        three_methods_run_together(ip_address, ip, port_test, self)
    else:
        two_methods_run_together(ip_address, ip, self)
