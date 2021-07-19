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
        self.step_attenuate = 80
        self.ip_izepto = ip_izepto
        self.ip_ibts = ip_ibts
        self.original_value = 867500000
        self.value = 855000000
        self.number_error_izepto = 0
        self.config_file = 0
        self.number_launch = 0
        self.time_start = 0
        self.data_file = 'filter.txt'
        self.config_file = "Orders.txt"
        self.frequency_step = 200000
        self.attenuate = 0
        self.stopping = 0

    def run(self):
        self.time_start = time.time()
        sensibility_result = open("Report_filter.txt", 'w+')  # preparation of the txt files
        sensibility_result.close()
        outfile = open(self.data_file, 'w+')
        outfile.close()
        write_doc("Sensitivity measurement iZepto")
        write_doc("Sensitivity measurement iBTS")
        self.launch_ibts()
        while self.value < 880000001:
            self.change_value()
            self.step_attenuate = 80
            self.attenuate = 0
            self.script()
            if self.stopping == 1:
                break
            self.value += self.frequency_step
        self.end_programme()

    def read_original_value(self):
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        cmd = "sed -n 16p /user/libsx1302-utils_V1.0.5-klk1-dirty/global_conf.json.sx1250.EU868"
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        wah = stdout.readline()
        self.original_value = wah[19:28]

    def change_value(self):
        self.read_original_value()
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        cmd = "sed -i '16 s/" + str(self.original_value) + "/" + str(self.value) + "/' /user/libsx1302-utils_V1.0.5" \
                                                                                   "-klk1-dirty/global_conf.json" \
                                                                                   ".sx1250.EU868 "
        ssh.exec_command(cmd, get_pty=True)

    def script(self):  # The script to test one channel
        for i in range(0, 1000):  # number of test, generally infinity
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
                    self.number_error_izepto += 1
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
            self.ready_ibts()
            time.sleep(1)  # 1 second of safety after that the ready_ibts function is completed
            ssh.close()
            a = stdout.readlines()
            number = round((len(a) / 4))
            result = (number / int(self.number_frames)) * 100
            write_doc("-----------------------------------")
            write_doc(round(result, 1))
            write_doc(self.step_attenuate)
            write_doc(self.value)
            write_doc(self.attenuate)
            write_doc("-----------------------------------")
            if round(result, 1) == 100 or self.step_attenuate == 1:
                logger.debug("---------------------------------")
                logger.debug(f"Test {i} of ∞ of frequency {self.value} Hz")
                logger.debug(
                    f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
                logger.debug(f"you send {self.number_frames} frames")
                logger.debug(f"you received {number} frames")
                logger.debug(f"The rate is : {round(result, 1)}%")
                logger.debug("---------------------------------")

                write_doc("---------------------------------")
                write_doc(f"Test {i} of infinity of frequency {self.value} Hz")
                write_doc(
                    f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
                write_doc(f"you send {self.number_frames} frames")
                write_doc(f"you received {number} frames")
                write_doc(f"The rate is : {round(result, 1)}%")
                write_doc("---------------------------------")
                self.write_data(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                                self.power)
                self.attenuate = float(self.attenuate) + self.step_attenuate  # The value of the frequency_step
                # increase of the step frequency_step value
                if round(result, 1) == 0:
                    # self.window.destroy()
                    break

            elif round(result, 1) == 0 and self.attenuate == 0 and self.value < 867500000:
                logger.debug("---------------------------------")
                logger.debug(f"Test {i} of ∞ of frequency {self.value} Hz")
                logger.debug(f"The frequency {self.value} is too far away from the filter, stepping forward...")
                logger.debug("---------------------------------")
                write_doc("---------------------------------")
                write_doc(f"Test {i} of infinity of frequency {self.value} Hz")
                write_doc(f"The frequency {self.value} is too far away from the filter, stepping forward...")
                write_doc("---------------------------------")
                break
            elif round(result, 1) == 0 and self.attenuate == 0 and self.value > 867500000:
                logger.debug("---------------------------------")
                logger.debug(f"Test {i} of ∞ of frequency {self.value} Hz")
                logger.debug(f"The frequency {self.value} is too far away from the filter, stopping...")
                logger.debug("---------------------------------")
                write_doc("---------------------------------")
                write_doc(f"Test {i} of infinity of frequency {self.value} Hz")
                write_doc(f"The frequency {self.value} is too far away from the filter, stopping...")
                write_doc("---------------------------------")
                self.stopping = 1
                break
            else:
                logger.debug("---------------------------------")
                logger.debug(f"Test {i} of ∞ of frequency {self.value} Hz")
                logger.debug(f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB is too "
                             f"high, stepping back...")
                logger.debug("---------------------------------")
                write_doc("---------------------------------")
                write_doc(f"Test {i} of infinity of frequency {self.value} Hz")
                write_doc(
                    f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB is too high, "
                    f"stepping back...")
                write_doc("---------------------------------")
                self.attenuate = float(self.attenuate) - self.step_attenuate
                if self.step_attenuate >= 20:
                    self.step_attenuate = self.step_attenuate / 2
                    self.attenuate = float(self.attenuate) + self.step_attenuate
                else:
                    if self.step_attenuate == 4:
                        self.step_attenuate = 1
                        self.attenuate = float(self.attenuate) + self.step_attenuate
                    else:
                        self.step_attenuate = 4
                        self.attenuate = float(self.attenuate) + self.step_attenuate

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

        frequency_label = Label(test_frame, text="Start frequency Hz :")
        frequency_label.grid(row=0, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        frequency = Entry(test_frame, cursor="right_ptr")
        frequency.grid(row=0, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        frequency.insert(0, 855000000)

        frequency_step_label = Label(test_frame, text="Frequency step Hz :")
        frequency_step_label.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        frequency_step = Entry(test_frame, cursor="right_ptr")
        frequency_step.grid(row=1, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        frequency_step.insert(0, 200000)

        attenuate_label = Label(test_frame, text="Quarter dB attenuation start :")
        attenuate_label.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate = Entry(test_frame, cursor="right_ptr")
        attenuate.grid(row=2, column=1, ipadx=0, ipady=0, padx=0, pady=0)
        attenuate.insert(0, 0)

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
                              command=lambda: [reset_all(sf, frequency_step, number_frames, attenuate, offset, bw,
                                                         frequency)])
        reset_button.pack(padx=0, pady=0, expand=True, fill="both", side=BOTTOM)

        start_button = Button(scale_frame, text="Start",
                              borderwidth=8, background=THE_COLOR,
                              activebackground="green", cursor="right_ptr", overrelief="sunken",
                              command=lambda: [self.lunch_safety_ibts(sf, frequency_step,
                                                                      number_frames,
                                                                      attenuate, offset, bw, power, frequency,
                                                                      new_window_ibts)])
        start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
        new_window_ibts.mainloop()

    def lunch_safety_ibts(self, sf, frequency_step, number_frames, attenuate, offset, bw, power, frequency,
                          new_window_main_graphic):  # a function to chek if all the values are correct
        try:  # to chek if the values are integer
            number_frames = float(number_frames.get())
            frequency_step = int(frequency_step.get())
            sf = float(sf.get())
            attenuate = float(attenuate.get())
            offset = float(offset.get())
            bw = int(bw.get())
            power = float(power.get())
            frequency = int(frequency.get())
            #  to chek if the values are conform
            if number_frames < 0 or number_frames > 1000000:
                logger.critical("Error, The number frames value is not conform")
                showerror("Error", "The number frames value is not conform")
            if frequency_step < 200000 or frequency_step > 1000000:
                logger.critical("Error, The frequency_step value is not conform")
                showerror("Error", "The frequency_step value is not conform")
            if sf < 6 or sf > 12:
                logger.critical("Error, The symbol rate value is not conform")
                showerror("Error", "The symbol rate value is not conform")
            if attenuate < 0 or attenuate > 359:
                logger.critical("Error, The step value is not conform")
                showerror("Error", "The step value is not conform")
            if offset < 0 or offset > 200:
                logger.critical("Error, The offset value is not conform")
                showerror("Error", "The offset value is not conform")
            if bw == 125 or bw == 250 or bw == 500:
                pass
            else:
                logger.critical("Error, The band width value is not conform")
                showerror("Error", "The band width value is not conform")
            if power < 0 or power > 100:
                logger.critical("Error, The power value is not conform")
                showerror("Error", "The power value is not conform")
            if frequency < 800000000 or frequency > 950000000:
                logger.critical("Error, The frequency value is not conform")
                showerror("Error", "The frequency value is not conform")
            else:
                new_window_main_graphic.destroy()
                self.number_frames = number_frames
                self.value = frequency
                self.frequency_step = frequency_step
                self.sf = sf
                self.attenuate = attenuate
                self.offset = offset
                self.bw = bw
                self.power = power
        except:
            logger.critical("Error, One or more of the values are not a number")
            showerror("Error", "One or more of the values are not a number")

    def ready_ibts(self):  # initialise the IBTS
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=self.ip_ibts, username=username, password=password)
        cmd = file_execution(self.config_file, 1).split(",")
        order = (cmd[0] + str(self.value / 1000000) + cmd[2] + str(self.bw) + cmd[4] + str(self.sf) + cmd[6] +
                 str(self.number_frames) + cmd[8] + str(abs(self.attenuate)))
        stdin, stdout, stderr = ssh2.exec_command(order, get_pty=True)
        while 1:
            read_value = stdout.readline()
            write_doc(read_value)
            #  logger.info(read_value)
            if read_value[3:5] == "27":
                logger.debug("The iBTS is ready")
                break
            if read_value[0:5] == "ERROR":
                self.attenuate = 0
                for t in range(0, 10):
                    logger.info("IBTS rebooting, it may take few minutes")
                    time.sleep(5)
                username = "root"
                password = "root"
                ssh2 = paramiko.SSHClient()
                ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh2.connect(hostname=self.ip_ibts, username=username, password=password)
                cmd = file_execution(self.config_file, 1).split(",")
                order = (cmd[0] + str(self.value / 1000000) + cmd[2] + str(self.bw) + cmd[4] + str(self.sf) + cmd[6] +
                         str(self.number_frames) + cmd[8] + str(self.attenuate))
                stdin, stdout, stderr = ssh2.exec_command(order, get_pty=True)
                while 1:
                    read_value = stdout.readline()
                    write_doc(read_value)
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
                      + ' ' + str(self.temperature_storage) +
                      ' ' + str(round(self.sf)) + ' ' + str(round(self.bw)) + ' ' + str(self.value) + ' ' +
                      "filter" + '\n')
        outfile.close()

    def end_programme(self):
        logger.debug("End test")
        logger.debug(f"Number of launch of the Izepto: {self.number_launch}")
        logger.debug(f"Number of fail of the Izepto: {self.number_error_izepto}")
        b = time.localtime(time.time() - self.time_start)  # Total time of the test
        logger.info(f'Test duration: {b[3] - 1}H{b[4]}min and {b[5]} second(s)')
        write_doc("End test")
        write_doc(f"Number of launch of the Izepto: {self.number_launch}")
        write_doc(f"Number of fail of the Izepto: {self.number_error_izepto}")
        write_doc(f'Test duration: {b[3] - 1}H{b[4]}min and {b[5]} second(s)')


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
    sensibility_result = open("Report_filter.txt", 'a')
    sensibility_result.write(str(text) + "\n")
    sensibility_result.close()


def reset_all(sf, attenuate, number_frames, step, offset, bw, frequency):
    number_frames.delete(0, 20)
    number_frames.insert(0, 100)
    attenuate.delete(0, 20)
    attenuate.insert(0, 280)
    sf.delete(0, 20)
    sf.insert(0, 7)
    step.delete(0, 20)
    step.insert(0, 4)
    offset.delete(0, 20)
    offset.insert(0, 60)
    bw.delete(0, 20)
    bw.insert(0, 125)
    frequency.delete(0, 20)
    frequency.insert(0, 855000000)
