#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 7 10:53:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
from loguru import logger
from tkinter import *
import sys
import paramiko

# =============================================================================
THE_COLOR = "#E76145"


def menu():
    window_graph_data = Tk()
    window_graph_data.title("Configuration file management")
    configuration_file_label = Label(window_graph_data, text="Select the name of the configuration file:")
    configuration_file_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    configuration_file = Entry(window_graph_data, cursor="right_ptr")
    configuration_file.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    configuration_file.insert(0, "Orders.txt")
    configuration_menu_button = Button(window_graph_data, text="Start analysis", borderwidth=8, background=THE_COLOR,
                                       cursor="right_ptr",
                                       overrelief="sunken",
                                       command=lambda: [file_execution(str(configuration_file.get())),
                                                        'window_graph_data.destroy()'])
    configuration_menu_button.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    reset_label = Label(window_graph_data, text="Reset The configuration file")
    reset_label.grid(row=3, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    reset_button = Button(window_graph_data, text="Reset", borderwidth=8, background=THE_COLOR,
                          cursor="right_ptr",
                          overrelief="sunken",
                          command=lambda: [file_reset()])
    reset_button.grid(row=4, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    reset_izepto_button = Button(window_graph_data, text="Reset Izepto configuration file", borderwidth=8,
                                 background=THE_COLOR,
                                 cursor="right_ptr",
                                 overrelief="sunken",
                                 command=lambda: [change_value()])
    reset_izepto_button.grid(row=4, column=1, ipadx=0, ipady=0, padx=0, pady=0)


def file_execution(file_name):
    file = open((sys.path[1]) + f"\\Order_files\\{file_name}", "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    logger.info(f"The file name is: {file_name}")
    for n in range(0, 2 * p, 2):
        logger.info(f"The command of the {donnees[n]} is: {donnees[n + 1]}")
    file.close()


def file_reset():
    file = open((sys.path[1]) + f"\\Order_files\\Orders.txt", "w+")
    file2 = open((sys.path[1]) + f"\\Order_files\\Orders_secure_save.txt", "r")
    for line in file2:
        file.write(str(line.rstrip('\n\r').split("=")[0] + "="))
        file.write(str(line.rstrip('\n\r').split("=")[1] + "\n"))
    file.close()
    file2.close()
    logger.info('Reset completed')


def file_reading(file_name, n):
    file = open((sys.path[1]) + f"\\Order_files\\{file_name}", "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    file.close()
    return donnees[n]


def read_original_value():
    username = "root"
    password = "root"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="192.168.4.183", username=username, password=password)
        cmd = file_reading("Orders.txt", 7)
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        wah = stdout.readline()
        return wah.split()
    except:
        logger.critical(f"Impossible to connected to 192.168.4.183")


def change_value():
    username = "root"
    password = "root"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname="192.168.4.183", username=username, password=password)
        cmd = file_reading("Orders.txt", 9).split(",")
        new_value_number = "867500000"
        order = (cmd[0] + str(read_original_value()[1][:-1]) + cmd[2] + new_value_number + cmd[4])
        ssh.exec_command(order, get_pty=True)
        logger.info("The reset of the configuration file of the Izepto is completed")
    except:
        logger.critical(f"Impossible to connected to 192.168.4.183")
