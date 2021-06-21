#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 18 14:11:00 2021
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
import time

# =============================================================================
THE_COLOR = "#E76145"


class Thread_sensibility(threading.Thread):

    def __init__(self, ip_address, ip, port_test):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip_address = ip_address
        self.ip = ip
        self.port_test = port_test
        self.attenuate = 0  # 0.25dB par pas

    def run(self):
        for i in range(0, 10):
            if i == 0:
                sensibility_result = open("Report_sensibility.txt", 'w+')
                sensibility_result.close()
                self.write_doc("Sensitivity measurement iZepto")
                self.write_doc("Sensitivity measurement iBTS")
            username = "root"
            password = "root"
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=username, password=password)
            cmd = "./lora_pkt_fwd -c global_conf.json.sx1250.EU868"
            cmd2 = "cd /user/libsx1302-utils_V1.0.5-klk1-dirty"
            stdin, stdout, stderr = ssh.exec_command(cmd2 + "\n" + cmd, get_pty=True)

            while (1):
                wah = stdout.readline()
                #  logger.info(wah)
                if wah[19:22] == "EUI":
                    logger.debug("The iZepto is ready")
                    break
            if i == 0:
                self.lunch_ibts()
            else:
                self.attenuate = int(self.attenuate) + 10
                self.ready_ibts()
            wah1 = 0
            time.sleep(1)
            for i in range(0, int(self.number_frames)):
                a = stdout.readline()
                wah1 = wah1 + 1
                #  logger.info(f"The number of frames receive is {wah1}")
            logger.debug("---------------------------------")
            logger.debug(f"Test {i} of {10}")
            logger.debug(f"The level of attenuation is : {self.attenuate} = {int(self.attenuate)/4} dB")
            logger.debug(f"you send {self.number_frames} frames")
            logger.debug(f"you received {wah1} frames")
            result = (wah1 / int(self.number_frames)) * 100
            logger.debug(f"The rate is : {result}%")
            logger.debug("---------------------------------")
            self.write_doc("---------------------------------")
            self.write_doc(f"Test {i} of {10}")
            self.write_doc(f"The level of attenuation is : {self.attenuate} = {int(self.attenuate)/4} dB")
            self.write_doc(f"you send {self.number_frames} frames")
            self.write_doc(f"you received {wah1} frames")
            self.write_doc(f"The rate is : {result}%")
            self.write_doc("---------------------------------")
            ssh.close()

    def lunch_ibts(self):
        new_window_main_graphic = Tk()
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

        frequency_label = Label(entry_frame, text="frequency channel :")
        frequency_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        frequency = Entry(entry_frame, cursor="right_ptr")
        frequency.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        frequency.insert(0, 867300000)

        sf_label = Label(entry_frame, text="Spreading factor 7 to 12:")
        sf_label.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        sf = Entry(entry_frame, cursor="right_ptr")
        sf.grid(row=2, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        sf.insert(0, 7)

        attenuate_label = Label(entry_frame, text="quarter dB attenuation :")
        attenuate_label.grid(row=3, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate = Entry(entry_frame, cursor="right_ptr")
        attenuate.grid(row=3, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate.insert(0, 0)

        reset_button = tk.Button(entry_frame, text="Reset",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.reset_all(frequency, sf, attenuate, number_frames)])
        reset_button.grid(row=5, column=0, ipadx=0, ipady=0, padx=0, pady=0)

        start_button = tk.Button(scale_frame, text="Start",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.lunch_safety(frequency, sf, attenuate, number_frames,
                                                                    new_window_main_graphic)])
        start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
        new_window_main_graphic.mainloop()

    def lunch_safety(self, frequency, sf, attenuate, number_frames, new_window_main_graphic):
        global is_killed
        try:  # to chek if the values are integer
            number_frames = int(number_frames.get())
            frequency = int(frequency.get())
            attenuate = int(attenuate.get())
            sf = int(sf.get())
            #  to chek if the values are conform
            if sf < 6 or sf > 12:
                logger.critical("Error, The symbol rate value is not conform")
                showerror("Error", "The symbol rate value is not conform")
            else:
                new_window_main_graphic.destroy()
                self.number_frames = str(number_frames)
                self.frequency = str(frequency / 1000000)
                self.attenuate = str(attenuate)
                self.sf = str(sf)
                self.ready_ibts()
        except:
            logger.critical("Error, One or more of the values are not a number")
            showerror("Error", "One or more of the values are not a number")

    def reset_all(self, frequency, sf, attenuate, number_frames):
        number_frames.delete(0, 20)
        number_frames.insert(0, 10)
        frequency.delete(0, 20)
        frequency.insert(0, 867300000)
        attenuate.delete(0, 20)
        attenuate.insert(0, 0)
        sf.delete(0, 20)
        sf.insert(0, 7)

    def write_doc(self, text):
        sensibility_result = open("Report_sensibility.txt", 'a')
        sensibility_result.write(str(text) + "\n")
        sensibility_result.close()

    def ready_ibts(self):
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_address, username=username, password=password)

        cmd = "/user/libloragw2-utils_5.1.0-klk9-3-ga23e25f_FTK_Tx/send_pkt -d " \
              "/dev/slot/1/spidev0 -f " + self.frequency + ":1:1 -a 0 -b 125 -s " + self.sf + "-c 1 -r 8 -z 20 -t 20 " \
                                                                                              "-x " + \
              self.number_frames + " --atten " + str(self.attenuate)

        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

        while 1:
            wah = stdout.readline()
            #  logger.info(wah)
            if wah[3:5] == "27":
                logger.debug("The iBTS is ready")
                break

