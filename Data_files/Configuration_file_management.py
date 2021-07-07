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
                                                        window_graph_data.destroy()])
    configuration_menu_button.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)


def file_execution(file_name):
    file = open((sys.path[1]) + f"\\Data_files\\{file_name}", "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    logger.info(f"The file name is: {file_name}")
    for n in range(0, 2 * p, 2):
        logger.info(f"The command of the {donnees[n]} is: {donnees[n + 1]}")
    file.close()