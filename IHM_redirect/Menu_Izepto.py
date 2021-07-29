#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 14 9:02:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from loguru import logger
import paramiko
from IHM_piloting.I_zepto import Izepto_script
from IHM import Graph_sensibility
import time
from tkinter import filedialog
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
# =============================================================================
THE_COLOR = "#E76145"
global status



def izepto_menu(self, ip_address):
    scanner_ibts_frame = LabelFrame(self, text="Detection of Izepto")
    scanner_ibts_frame.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    izepto_scale_frame = LabelFrame(self, text="Start the test")
    izepto_scale_frame.grid(row=0, column=2, ipadx=0, ipady=0, padx=0, pady=0)
    reboot_scale_frame = LabelFrame(self, text="reboot_izepto")
    reboot_scale_frame.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    make_a_graph = LabelFrame(self, text="Make a graph")
    make_a_graph.grid(row=1, column=2, ipadx=0, ipady=0, padx=0, pady=0)
    start_test_button = tk.Button(izepto_scale_frame, text="Ignition of the card",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [call_graph_izepto(ip_address, port_com_frame_entry,
                                                                     visual_color_button_sg, izepto_info_label)])
    start_test_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    reboot_button = tk.Button(reboot_scale_frame, text="Reboot the card",
                                  borderwidth=8, background=THE_COLOR,
                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                  command=lambda: [reboot(port_com_frame_entry)])
    reboot_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)
    place = scanner_ibts_frame
    scanner_port_com_frame_label = Label(place, text="Select your IP address:")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_entry = Entry(place)
    port_com_frame_entry.pack(padx=0, pady=10, expand=False, fill="none", side=TOP)
    port_com_frame_entry.insert(0, ip_address)
    port_com_frame_button = Button(place, text="Connect", borderwidth=8, background=THE_COLOR,
                                   activebackground="green", disabledforeground="grey",
                                   cursor="right_ptr",
                                   overrelief="sunken",
                                   command=lambda: [try_izepto_connection(port_com_frame_entry,
                                                                          port_com_frame_entry_name,
                                                                          visual_color_button_sg)])
    port_com_frame_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="The currently selected IP address :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    port_com_frame_entry_name = Label(place, text=ip_address)
    port_com_frame_entry_name.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    scanner_port_com_frame_label = Label(place, text="Connection status :")
    scanner_port_com_frame_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    visual_color_button_sg = Button(place, state="disabled", disabledforeground="black")
    visual_color_button_sg.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    izepto_info_label = Button(place, text="The Izepto card is not ready", disabledforeground="black",
                               bg="red", state="disabled")
    izepto_info_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    try_izepto_connection(port_com_frame_entry,
                          port_com_frame_entry_name,
                          visual_color_button_sg)
    make_a_graph_button = tk.Button(make_a_graph, text="Draw",
                                    borderwidth=8, background=THE_COLOR,
                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                    command=lambda: [Graph_sensibility.draw_graph(self)])
    make_a_graph_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)


def visual_function(visual_color_button, s):
    if s == 1:
        visual_color_button.config(text="The connection status is : offline", bg="red")
    else:
        visual_color_button.config(text="The connection status is : online", bg="light green")

def reboot(port_com_frame_entry):
    ip_address = port_com_frame_entry.get()
    username = "root"
    password = "root"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        cmd = "reboot"
        ssh.exec_command(cmd, get_pty=True)
        logger.info(f"rebooting {ip_address}, it may take few minutes")
        for t in range(0, 10):
            logger.info("Izepto rebooting, it may take few minutes")
            time.sleep(5)
        logger.debug("The iZepto is ready")
    except:
        logger.error("Invalid ip_izepto adress")


def try_izepto_connection(port_com_frame_entry, port_com_frame_entry_name, visual_color_button_sg):
    global status
    ip_address = port_com_frame_entry.get()
    try:
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        status = 1
        visual_function(visual_color_button_sg, 0)
        logger.debug("The connection was correctly established")
    except:
        status = 0
        visual_function(visual_color_button_sg, 1)
        logger.critical(f"The IP address [{ip_address}] is not link to the IBTS")
    finally:
        port_com_frame_entry_name.config(text=ip_address)


def call_graph_izepto(ip_address, port_com_frame_entry, visual_color_button_sg, izepto_info_label):
    global status
    change_izepto(port_com_frame_entry.get(), visual_color_button_sg)
    if status == 0:
        if askyesno("Warning", "The connection status is : offline\n Do you still want to continue ?"):
            Izepto_script.lunch_izepto(ip_address, 0)
            #ask_order_file(ip_address)
        else:
            visual_function(visual_color_button_sg, 1)
    else:
        Izepto_script.lunch_izepto(ip_address, 0)
        #ask_order_file(ip_address)
        izepto_info_label.config(text="The Izepto card is ready to received", bg="light green")

def change_izepto(name, visual_color_button_sg):
    global status
    ip_address = name
    try:
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        status = 1
        visual_function(visual_color_button_sg, 0)
    except:
        status = 0
        logger.critical(f"The IP address [{ip_address}] is not link to the izepto")

def ask_order_file(ip_address):

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
                          command=lambda: [verification(ip_address, str(configuration_file.get()), window_graph_data)])
    check_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

def verification(ip_address, file_name, window_graph_data):
    try:
        data = pd.read_csv(file_name, sep='\s+', header=None)
        data = pd.DataFrame(data)
        a = file_name.split('/')
        if a[-1] == 'Orders.txt':
            Izepto_script.lunch_izepto(ip_address, file_name)
            window_graph_data.destroy()
        else:
            logger.critical(f"The file is not 'Orders.txt'")
    except:
        logger.critical(f"The file name {file_name} is invalid")