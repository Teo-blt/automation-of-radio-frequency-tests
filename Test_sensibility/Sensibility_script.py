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


class Threadsensibility(threading.Thread):

    def __init__(self, ip_address, ip, port_test):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip_address = ip_address
        self.ip = ip
        self.port_test = port_test
        self.attenuate = 0  # 0.25dB par pas
        self.number_frames = 0
        self.frequency = 0
        self.attenuate = 0
        self.sf = 0
        self.step = 0
        self.offset = 0
        self.test = 0
        self.bw = 0

    def run(self):
        self.lunch_ibts()
        for i in range(0, int(self.test)):
            if i == 0:
                sensibility_result = open("Report_sensibility.txt", 'w+')
                sensibility_result.close()
                outfile = open('test.txt', 'w+')
                outfile.close()
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

            while 1:
                wah = stdout.readline()
                #  logger.info(wah)
                if wah[19:22] == "EUI":
                    logger.debug("The iZepto is ready")
                    break
            if i == 0:
                self.ready_ibts()
            else:
                self.attenuate = float(self.attenuate) + self.step
                self.ready_ibts()
            time.sleep(1)
            ssh.close()
            a = stdout.readlines()
            number = (len(a) / 4)
            logger.debug("---------------------------------")
            logger.debug(f"Test {i} of {self.test}")
            logger.debug(f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
            logger.debug(f"you send {self.number_frames} frames")
            logger.debug(f"you received {number} frames")
            result = (number / int(self.number_frames)) * 100
            logger.debug(f"The rate is : {round(result, 1)}%")
            logger.debug("---------------------------------")
            self.write_doc("---------------------------------")
            self.write_doc(f"Test {i} of {10}")
            self.write_doc(
                f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
            self.write_doc(f"you send {self.number_frames} frames")
            self.write_doc(f"you received {number} frames")
            self.write_doc(f"The rate is : {result}%")
            self.write_doc("---------------------------------")
            self.write_json(round(float(self.attenuate) / 4 + int(self.offset), 1), 100 - round(result, 1))
            if round(result, 1) == 0:
                logger.debug("fin")
                self.write_doc("fin")
                break

    def lunch_ibts(self):
        new_window_main_graphic = Tk()
        new_window_main_graphic.title("Signal generator settings")

        settings_frame = LabelFrame(new_window_main_graphic, text="Settings")
        settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        settings_frame.config(background='#fafafa')

        scale_frame = LabelFrame(settings_frame, bd=0)  # , text="Scales"
        scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
        scale_frame.config(background='#fafafa')

        transmitter_frame = LabelFrame(scale_frame, text="Transmitter settings")
        transmitter_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)

        test_frame = LabelFrame(scale_frame, text="Test settings")
        test_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)

        packet_frame = LabelFrame(scale_frame, text="Packet settings")
        packet_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)

        test_label = Label(test_frame, text="Number of tests")
        test_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        test = Entry(test_frame, cursor="right_ptr")
        test.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        test.insert(0, -1)

        attenuate_label = Label(test_frame, text="Quarter dB attenuation start :")
        attenuate_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate = Entry(test_frame, cursor="right_ptr")
        attenuate.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate.insert(0, 280)

        step_label = Label(test_frame, text="Step of quarter dB attenuation :")
        step_label.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        step = Entry(test_frame, cursor="right_ptr")
        step.grid(row=2, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        step.insert(0, 4)

        power_label = Label(transmitter_frame, text="Power of the transmitter in dBm")
        power_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        power = Entry(transmitter_frame, cursor="right_ptr")
        power.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        power.insert(0, 5)

        offset_label = Label(transmitter_frame, text="Offset dB :")
        offset_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        offset = Entry(transmitter_frame, cursor="right_ptr")
        offset.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        offset.insert(0, 60)

        number_frames_label = Label(packet_frame, text="Number of sent frames :")
        number_frames_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        number_frames = Entry(packet_frame, cursor="right_ptr")
        number_frames.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        number_frames.insert(0, 100)

        frequency_label = Label(packet_frame, text="frequency channel :")
        frequency_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        frequency = Entry(packet_frame, cursor="right_ptr")
        frequency.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        frequency.insert(0, 867300000)

        sf_label = Label(packet_frame, text="Spreading factor 7 to 12:")
        sf_label.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        sf = Entry(packet_frame, cursor="right_ptr")
        sf.grid(row=2, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        sf.insert(0, 7)

        bw_label = Label(packet_frame, text="band width:")
        bw_label.grid(row=3, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        bw = Entry(packet_frame, cursor="right_ptr")
        bw.grid(row=3, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        bw.insert(0, 125)

        reset_button = tk.Button(scale_frame, text="Reset",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.reset_all(frequency, sf, attenuate,
                                                                 number_frames, step, offset, test, bw)])
        reset_button.pack(padx=0, pady=0, expand=True, fill="both", side=BOTTOM)

        start_button = tk.Button(scale_frame, text="Start",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.lunch_safety(frequency, sf, attenuate, number_frames,
                                                                    step, offset, test, bw, power,
                                                                    new_window_main_graphic)])
        start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
        new_window_main_graphic.mainloop()

    def lunch_safety(self, frequency, sf, attenuate, number_frames, step, offset, test, bw, power,
                     new_window_main_graphic):
        global is_killed
        try:  # to chek if the values are integer
            number_frames = float(number_frames.get())
            frequency = float(frequency.get())
            attenuate = float(attenuate.get())
            sf = float(sf.get())
            step = float(step.get())
            offset = float(offset.get())
            test = float(test.get())
            bw = float(bw.get())
            power = float(power.get())
            #  to chek if the values are conform
            if number_frames < 0 or number_frames > 1000000:
                logger.critical("Error, The number frames value is not conform")
                showerror("Error", "The number frames value is not conform")
            if frequency < 0 or frequency > 10000000000:
                logger.critical("Error, The frequency value is not conform")
                showerror("Error", "The frequency value is not conform")
            if attenuate < 0 or attenuate > 1000000:
                logger.critical("Error, The attenuate value is not conform")
                showerror("Error", "The attenuate value is not conform")
            if sf < 6 or sf > 12:
                logger.critical("Error, The symbol rate value is not conform")
                showerror("Error", "The symbol rate value is not conform")
            if step < 0 or step > 10000000:
                logger.critical("Error, The step value is not conform")
                showerror("Error", "The step value is not conform")
            if offset < 0 or offset > 10000000:
                logger.critical("Error, The offset value is not conform")
                showerror("Error", "The offset value is not conform")
            if test < 0 or test > 10000000:
                if test == -1:
                    test = 1000
                else:
                    logger.critical("Error, The test value is not conform")
                    showerror("Error", "The test value is not conform")
            if bw < 0 or bw > 10000000:
                logger.critical("Error, The band width value is not conform")
                showerror("Error", "The band width value is not conform")
            if power < 0 or power > 10000000:
                logger.critical("Error, The power value is not conform")
                showerror("Error", "The power value is not conform")
            else:
                new_window_main_graphic.destroy()
                self.number_frames = number_frames
                self.frequency = frequency / 1000000
                self.attenuate = attenuate
                self.sf = sf
                self.step = step
                self.offset = offset
                self.test = test
                self.bw = bw
                self.power = power
        except:
            logger.critical("Error, One or more of the values are not a number")
            showerror("Error", "One or more of the values are not a number")

    def reset_all(self, frequency, sf, attenuate, number_frames, step, offset, test, bw):
        number_frames.delete(0, 20)
        number_frames.insert(0, 100)
        frequency.delete(0, 20)
        frequency.insert(0, 867300000)
        attenuate.delete(0, 20)
        attenuate.insert(0, 280)
        sf.delete(0, 20)
        sf.insert(0, 7)
        step.delete(0, 20)
        step.insert(0, 4)
        offset.delete(0, 20)
        offset.insert(0, 60)
        test.delete(0, 20)
        test.insert(0, -1)
        bw.delete(0, 20)
        bw.insert(0, 125)

    def write_doc(self, text):
        sensibility_result = open("Report_sensibility.txt", 'a')
        sensibility_result.write(str(text) + "\n")
        sensibility_result.close()

    def write_json(self, text1, text2):
        outfile = open('test.txt', 'a')
        outfile.write(str(text1) + ' ' + str(text2) + '\n')
        outfile.close()

    def ready_ibts(self):
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=self.ip_address, username=username, password=password)
        cmd = "/user/libloragw2-utils_5.1.0-klk9-3-ga23e25f_FTK_Tx/send_pkt -d " \
              "/dev/slot/1/spidev0 -f " + str(self.frequency) + ":1:1 -a 0 -b " + str(self.bw) + " -s " + str(
            self.sf) + "-c 1 -r 8 " \
                       "-z 20 -t " \
                       "20 " \
                       "-x " + \
              str(self.number_frames) + " --atten " + str(self.attenuate)

        stdin, stdout, stderr = ssh2.exec_command(cmd, get_pty=True)

        while 1:
            wah = stdout.readline()
            #  logger.info(wah)
            if wah[3:5] == "27":
                logger.debug("The iBTS is ready")
                break
        wah1 = 0
        while wah1 != int("%d" % int(self.number_frames)):
            a = stdout.read(1)
            if a == b'X':
                wah1 = wah1 + len(a)
            else:
                pass
        logger.debug("All frames send")
        ssh2.close()
