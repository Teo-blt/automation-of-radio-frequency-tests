#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 13 15:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import paramiko
from loguru import logger
import threading
import time
import sys
from tkinter.messagebox import *
from tkinter import *

# =============================================================================
THE_COLOR = "#E76145"


class Threadfilter(threading.Thread):

    def __init__(self, ip_izepto, ip_ibts):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.bw = 0
        self.sf = 0
        self.temperature_storage = 0
        self.climate_chamber_num = 0
        self.power = 0
        self.number_frames = 0
        self.offset = 0
        self.value_mono_multi = 0
        self.step_attenuate = 0
        self.attenuate_storage = 0
        self.ip_izepto = ip_izepto
        self.ip_ibts = ip_ibts
        self.original_value = 867500000
        self.value = 855000000
        self.test = 0
        self.frequency = 0
        self.number_error = 0
        self.config_file = 0
        self.number_launch = 0
        self.time_start = 0
        self.data_file = 'filter.txt'
        self.config_file = "Orders.txt"

    def run(self):
        self.time_start = time.time()
        sensibility_result = open("Report_filter.txt", 'w+')  # preparation of the txt files
        sensibility_result.close()
        outfile = open(self.data_file, 'w+')
        outfile.close()
        write_doc("Sensitivity measurement iZepto")
        write_doc("Sensitivity measurement iBTS")
        self.launch_ibts()
        while self.value < 880200000:
            self.change_value()
            self.value += 200000

    def read_original_value(self):
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        cmd = "sed -n 6p /etc/lorad/zepto/EU868-FR.json"
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        wah = stdout.readline()
        self.original_value = wah

    def change_value(self):
        self.read_original_value()
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        logger.debug(f"Successfully connected to {self.ip_izepto}")
        cmd = "sed -i '6 s/" + str(self.original_value) + "/" + str(self.value) + "/' /etc/lorad/zepto/EU868-FR.json"
        ssh.exec_command(cmd, get_pty=True)

    def script(self):  # The script to test one channel
        for i in range(0, int(self.test)):  # number of test, generally infinity
            username = "root"
            password = "root"
            ssh = paramiko.SSHClient()  # initialisation de la liaison SSH
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip_izepto, username=username, password=password)
            cmd = file_execution(self.config_file, 3) + "\n" + file_execution(self.config_file, 5)
            stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
            while 1:
                response = stdout.readline()
                if response[0:5] == "ERROR":
                    self.number_error += 1
                    logger.critical("---------------------------------")
                    logger.critical("Failed to start the concentrator")
                    logger.critical("The Izepto is rebooting, please standby")
                    logger.critical("---------------------------------")
                    write_doc("---------------------------------")
                    write_doc("Failed to start the concentrator")
                    write_doc("The Izepto is rebooting, please standby")
                    write_doc("---------------------------------")
                    ssh.exec_command("reboot", get_pty=True)
                    for t in range(0, 10):
                        logger.info("Izepto rebooting, it may take few minutes")
                        time.sleep(5)
                    username = "root"
                    password = "root"
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.ip_izepto, username=username, password=password)
                    cmd = file_execution(self.config_file, 3) + "\n" + file_execution(self.config_file, 5)
                    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
                    if response[19:22] == "EUI":
                        logger.debug("The iZepto is ready")
                        logger.debug("The reboot is completed")
                        write_doc("The reboot is completed")
                        break
                if response[19:22] == "EUI":
                    logger.debug("The iZepto is ready")
                    self.number_launch += 1
                    break
            if i == 0:
                self.attenuate = self.attenuate_storage
                self.ready_ibts()  # lunch the initialisation of the IBTS
            else:
                self.attenuate = float(self.attenuate) + self.step_attenuate  # The value of the attenuate increase of
                # the step attenuate value
                self.ready_ibts()
            time.sleep(1)  # 1 second of safety after that the ready_ibts function is completed
            ssh.close()
            a = stdout.readlines()
            number = round((len(a) / 4))
            logger.debug("---------------------------------")
            if int(self.test) == 1000:
                logger.debug(f"Test {i} of ∞ of channel number: {self.value_mono_multi}")
            else:
                logger.debug(f"Test {i} of {self.test}")
            logger.debug(
                f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
            logger.debug(f"you send {self.number_frames} frames")
            logger.debug(f"you received {number} frames")
            result = (number / int(self.number_frames)) * 100
            logger.debug(f"The rate is : {round(result, 1)}%")
            logger.debug("---------------------------------")

            write_doc("---------------------------------")
            if int(self.test) == 1000:
                write_doc(f"Test {i} of infinity of channel number: {self.value_mono_multi}")
            else:
                write_doc(f"Test {i} of {self.test}")
            write_doc(
                f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
            write_doc(f"you send {self.number_frames} frames")
            write_doc(f"you received {number} frames")
            write_doc(f"The rate is : {round(result, 1)}%")
            write_doc("---------------------------------")
            self.write_data(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                            self.power)
            if round(result, 1) == 0:
                logger.debug(f"fin channel number: {self.value_mono_multi}\n")
                write_doc(f"fin channel number: {self.value_mono_multi}\n")
                # self.window.destroy()
                break

    def launch_ibts(self):  # lunch the IBTS settings menu
        new_window_ibts = Tk()
        new_window_ibts.title("Signal generator settings")

        settings_frame = LabelFrame(new_window_ibts, text="Settings")
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
        self.frequency_entry = Entry(packet_frame, cursor="right_ptr")
        self.frequency_entry.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        self.frequency_entry.insert(0, 867100000)

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
        reset_button = Button(scale_frame, text="Reset",
                              borderwidth=8, background=THE_COLOR,
                              activebackground="green", cursor="right_ptr", overrelief="sunken",
                              command=lambda: [self.reset_all(self.frequency_entry, sf, attenuate,
                                                              number_frames, step, offset, test, bw)])
        reset_button.pack(padx=0, pady=0, expand=True, fill="both", side=BOTTOM)

        start_button = Button(scale_frame, text="Start",
                              borderwidth=8, background=THE_COLOR,
                              activebackground="green", cursor="right_ptr", overrelief="sunken",
                              command=lambda: [self.lunch_safety_ibts(self.frequency_entry, sf, attenuate,
                                                                      number_frames,
                                                                      step, offset, test, bw, power,
                                                                      new_window_ibts)])
        start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
        new_window_ibts.mainloop()

    def lunch_safety_ibts(self, frequency, sf, attenuate, number_frames, step, offset, test, bw, power,
                          new_window_main_graphic):  # a function to chek if all the values are correct
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
                self.frequency_storage = frequency / 1000000
                self.attenuate = attenuate
                self.attenuate_storage = attenuate
                self.sf = sf
                self.step_attenuate = step
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
        frequency.insert(0, 867100000)
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

    def ready_ibts(self):  # initialise the IBTS
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=self.ip_ibts, username=username, password=password)

        cmd = file_execution(self.config_file, 1).split(",")
        order = (cmd[0] + str(self.frequency) + cmd[2] + str(self.bw) + cmd[4] + str(self.sf) + cmd[6] +
                 str(self.number_frames) + cmd[8] + str(self.attenuate))
        stdin, stdout, stderr = ssh2.exec_command(order, get_pty=True)

        while 1:
            read_value = stdout.readline()
            #  logger.info(read_value)
            if read_value[3:5] == "27":
                logger.debug("The iBTS is ready")
                break
        read_value_2 = 0
        while read_value_2 != int("%d" % int(self.number_frames)):
            a = stdout.read(1)
            if a == b'X':
                read_value_2 = read_value_2 + len(a)
            else:
                pass
        logger.debug("All frames send")
        ssh2.close()

    def write_data(self, attenuation_db, packet_lost, power_out):
        outfile = open(self.data_file, 'a')
        power_in = round(power_out - attenuation_db, 2)
        outfile.write(str(power_in) + ' ' + str(round(packet_lost)) + ' ' + str(self.climate_chamber_num)
                      + ' ' + str(self.value_mono_multi) + ' ' + str(self.temperature_storage) +
                      ' ' + str(round(self.sf)) + ' ' + str(round(self.bw)) + '\n')
        outfile.close()


def file_execution(file_name, n):
    file = open((sys.path[1]) + f"\\Data_files\\{file_name}", "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    file.close()
    return donnees[n]


def write_doc(text):
    sensibility_result = open("Report_sensibility.txt", 'a')
    sensibility_result.write(str(text) + "\n")
    sensibility_result.close()
