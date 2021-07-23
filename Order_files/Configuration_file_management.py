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
from tkinter import filedialog
import pandas as pd
# =============================================================================
THE_COLOR = "#E76145"

def menu():
    window_graph_data = Tk()
    info_selection = LabelFrame(window_graph_data, text="Info selection")
    menu_frame = LabelFrame(window_graph_data, text="Menu")
    menu_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    choice_frame = LabelFrame(window_graph_data, text="Choice")
    window_graph_data.title("Configuration file management")
    configuration_file_label = Label(menu_frame, text="Select the name of the configuration file:")
    configuration_file_label.pack(expand=False, fill="none", side=TOP)
    configuration_file = Entry(menu_frame, cursor="right_ptr")
    configuration_file.pack(expand=False, fill="none", side=TOP)
    configuration_file.insert(0, "Select command file")
    configuration_menu_button = Button(choice_frame, text="Start analysis", borderwidth=8, background=THE_COLOR,
                                       cursor="right_ptr",
                                       overrelief="sunken",
                                       command=lambda: [file_execution(str(configuration_file.get()))])
    configuration_menu_button.grid(row=0, column=1, ipadx=10, ipady=10, padx=10, pady=10)
    reset_button = Button(choice_frame, text="Reset command file", borderwidth=8, background=THE_COLOR,
                          cursor="right_ptr",
                          overrelief="sunken",
                          command=lambda: [file_reset(str(configuration_file.get()))])
    reset_button.grid(row=1, column=0, ipadx=10, ipady=10, padx=10, pady=10)
    reset_izepto_button = Button(choice_frame, text="Reset Izepto configuration file", borderwidth=8,
                                 background=THE_COLOR,
                                 cursor="right_ptr",
                                 overrelief="sunken",
                                 command=lambda: [change_value()])
    reset_izepto_button.grid(row=1, column=1, ipadx=10, ipady=10, padx=10, pady=10)
    info_file_name_label = Label(info_selection, text="Actual file :")
    info_file_name_label.pack(expand=False, fill="none", side=TOP)
    info_label = Label(info_selection, text="")
    info_label.pack(expand=False, fill="none", side=TOP)

    def uploadaction(file_entry):
        filename = filedialog.askopenfilename(filetypes=[("text files", ".txt")])
        file_entry.delete(0, 2000)
        file_entry.insert(0, filename)

    def verification(file_name):
        try:
            data = pd.read_csv(file_name, sep='\s+', header=None)
            data = pd.DataFrame(data)
            a = file_name.split('/')
            if a[-1] == 'Orders.txt':
                menu_frame.grid_forget()
                choice_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
                info_selection.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
                info_label.config(text=file_name.split("/")[-1])
            else:
                logger.critical(f"The file is not 'Orders.txt'")
        except:
            logger.critical(f"The file name {file_name} is invalid")



    import_file_button = Button(menu_frame, text="Import file",
                                borderwidth=8, background=THE_COLOR,
                                activebackground="green", cursor="right_ptr", overrelief="sunken",
                                command=lambda: [uploadaction(configuration_file)])
    import_file_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    check_button = Button(menu_frame, text="Check file",
                          borderwidth=8, background=THE_COLOR,
                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                          command=lambda: [verification(configuration_file.get())])
    check_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    back_button = Button(choice_frame, text="Back",
                         borderwidth=8, background=THE_COLOR,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [go_back()])
    back_button.grid(row=0, column=0, ipadx=10, ipady=10, padx=10, pady=10)

    def go_back():
        choice_frame.grid_forget()
        info_selection.grid_forget()
        menu_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)



def file_execution(file_name):
    file = open(file_name, "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    logger.info(f"The file name is: {file_name}")
    for n in range(0, 2 * p, 2):
        logger.info(f"The command of the {donnees[n]} is: {donnees[n + 1]}")
    file.close()


def file_reset(file_name):
    file = open(file_name, "w+")
    file2 = open(file_name[:-10] + f"/Orders_secure_save.txt", "r")
    for line in file2:
        file.write(str(line.rstrip('\n\r').split("=")[0] + "="))
        file.write(str(line.rstrip('\n\r').split("=")[1] + "\n"))
    file.close()
    file2.close()
    logger.info('Reset completed')


def file_reading(file_name, n):
    file = open(file_name, "r")
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
