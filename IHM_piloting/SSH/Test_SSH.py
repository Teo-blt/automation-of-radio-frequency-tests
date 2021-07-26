#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 10 15:25:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import paramiko
import threading
from tkinter import *
import tkinter as tk
from loguru import logger
from tkinter.messagebox import *
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
# =============================================================================
global is_killed
is_killed = 0
THE_COLOR = "#E76145"


def lunch_ibts(ip, file_name):
    new_window_main_graphic = tk.Toplevel()
    new_window_main_graphic.title("Signal generator settings")

    settings_frame = LabelFrame(new_window_main_graphic, text="Settings")
    settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    settings_frame.config(background='#fafafa')

    scale_frame = LabelFrame(settings_frame, bd=0)  # , text="Scales"
    scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_frame.config(background='#fafafa')

    entry_frame = LabelFrame(scale_frame, text="Entry settings")
    entry_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)

    number_frames_label = Label(entry_frame, text="Number of sent frames :")
    number_frames_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    number_frames = Entry(entry_frame, cursor="right_ptr")
    number_frames.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    number_frames.insert(0, 10)

    frequency_label = Label(entry_frame, text="Frequency channel :")
    frequency_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    frequency = Entry(entry_frame, cursor="right_ptr")
    frequency.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    frequency.insert(0, 867300000)

    sf_label = Label(entry_frame, text="Spreading factor 7 to 12:")
    sf_label.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    sf = Entry(entry_frame, cursor="right_ptr")
    sf.grid(row=2, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    sf.insert(0, 7)

    attenuate_label = Label(entry_frame, text="Quarter dB attenuation :")
    attenuate_label.grid(row=3, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    attenuate = Entry(entry_frame, cursor="right_ptr")
    attenuate.grid(row=3, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    attenuate.insert(0, 0)

    bw_label = Label(entry_frame, text="Band with :")
    bw_label.grid(row=4, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    bw = Entry(entry_frame, cursor="right_ptr")
    bw.grid(row=4, column=1, ipadx=0, ipady=0, padx=0, pady=0)
    bw.insert(0, 125)

    reset_button = tk.Button(entry_frame, text="Reset",
                             borderwidth=8, background=THE_COLOR,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [reset_all(frequency, sf, attenuate, number_frames, bw)])
    reset_button.grid(row=5, column=0, ipadx=0, ipady=0, padx=0, pady=0)

    start_button = tk.Button(scale_frame, text="Start",
                             borderwidth=8, background=THE_COLOR,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [lunch_safety(frequency, sf, attenuate, number_frames, ip, bw, file_name)])
    start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)


def lunch_safety(frequency, sf, attenuate, number_frames, ip, bw, file_name):
    global is_killed
    try:  # to chek if the values are integer
        number_frames = float(number_frames.get())
        frequency = float(frequency.get())
        attenuate = float(attenuate.get())
        sf = float(sf.get())
        bw = float(bw.get())
        #  to chek if the values are conform
        if number_frames < 0 or number_frames > 1000000:
            logger.critical("Error, The number frames value is not conform")
            showerror("Error", "The number frames value is not conform")
        if frequency < 0 or frequency > 10000000000:
            logger.critical("Error, The frequency value is not conform")
            showerror("Error", "The frequency value is not conform")
        if attenuate < 0 or attenuate > 1000000:
            logger.critical("Error, The frequency_step value is not conform")
            showerror("Error", "The frequency_step value is not conform")
        if sf < 6 or sf > 12:
            logger.critical("Error, The symbol rate value is not conform")
            showerror("Error", "The symbol rate value is not conform")
        if bw < 0 or bw > 10000000:
            logger.critical("Error, The band with value is not conform")
            showerror("Error", "The band with value is not conform")
        else:
            if is_killed == 0:
                is_killed = 1
                Threadibts(frequency, sf, attenuate, number_frames, bw, ip, file_name).start()
            else:
                logger.info("The smiq program is already running")
    except:
        logger.critical("Error, One or more of the values are not a number")
        showerror("Error", "One or more of the values are not a number")


def reset_all(frequency, sf, attenuate, number_frames, bw):
    number_frames.delete(0, 20)
    number_frames.insert(0, 10)
    frequency.delete(0, 20)
    frequency.insert(0, 867300000)
    attenuate.delete(0, 20)
    attenuate.insert(0, 0)
    sf.delete(0, 20)
    sf.insert(0, 7)
    bw.delete(0, 20)
    bw.insert(0, 125)


class Threadibts(threading.Thread):

    def __init__(self, frequency, sf, attenuate, number_frames, bw, ip, file_name):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.frequency = str(frequency / 1000000)  # Number of sent frames
        self.sf = str(sf)
        self.attenuate = str(attenuate)
        self.number_frames = str(number_frames)
        self.bw = str(bw)
        self.ip = ip
        self.file_name = file_name

    def run(self):
        global is_killed
        ibts_result = open("Report_iBTS.txt", 'w+')
        ibts_result.close()
        ip_address = self.ip
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        logger.debug("Successfully connected to", ip_address)

        cmd = self.file_execution(self.file_name, 1).split(",")
        order = (cmd[0] + self.frequency + cmd[2] + self.bw + cmd[4] + self.sf + cmd[6] + self.number_frames + cmd[8]
                 + self.attenuate)

        stdin, stdout, stderr = ssh.exec_command(order, get_pty=True)

        while 1:
            wah = stdout.readline()
            logger.info(wah)
            if wah[3:5] == "27":
                logger.debug("The iBTS is ready")
                break
        wah1 = 0
        while wah1 != int("%d" % float(self.number_frames)):
            a = stdout.read(1)
            if a == b'X':
                wah1 = wah1 + len(a)
            else:
                pass
        logger.info(f"{self.number_frames} frames have been sent at -{float(self.attenuate) / 4} dB")
        ssh.close()
        is_killed = 0

    def file_execution(self, file_name, n):
        file = open(file_name, "r")
        donnees = []
        p = 0
        for line in file:
            donnees = donnees + line.rstrip('\n\r').split("=")
            p += 1
        file.close()
        return (donnees[n])
