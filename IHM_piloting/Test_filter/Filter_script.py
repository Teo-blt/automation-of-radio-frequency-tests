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
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
# =============================================================================
THE_COLOR = "#E76145"
CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
vt = serial.Serial()


class Threadfilter(threading.Thread):

    def __init__(self, ip_izepto, ip_ibts, port_test, file_name):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.step_temp = 0
        self.t_end = 0
        self.t_start = 0
        self.a = 0
        self.time_temp_wait = 0
        self.temp = 0
        self.temp2 = 0
        self.temperature = 0
        self.value_mono_multi = 0
        self.VALUE_STABILISATION = 0
        self.port_test = port_test
        self.bw = 0
        self.sf = 0
        self.value_storage = 0
        self.temperature_storage = 0
        self.climate_chamber_num = 0
        self.power = 0
        self.number_frames = 0
        self.offset = 0
        self.step_attenuate = 80
        self.ip_izepto = ip_izepto
        self.ip_ibts = ip_ibts
        self.original_value = []
        self.value = 855000000
        self.number_error_izepto = 0
        self.config_file = 0
        self.number_launch = 0
        self.time_start = 0
        self.report_file = "Report_filter.txt"
        self.data_file = 'Data_filter.txt'
        self.config_file = file_name
        self.frequency_step = 200000
        self.attenuate = 0
        self.stopping = 0
        self.reponse_storage_izepto = []
        self.reponse_storage_ibts = []
        self.file_path = ''

    def run(self):
        self.time_start = time.time()
        self.name_files()
        sensibility_result = open(self.report_file, 'x')  # preparation of the txt files
        sensibility_result.close()
        outfile = open(self.data_file, 'x')
        outfile.close()
        self.write_doc("Sensitivity measurement iZepto")
        self.write_doc("Sensitivity measurement iBTS")
        self.launch_ibts()
        if self.port_test != -1:  # to choose il the climate chamber need to be used
            self.launch_climatic_chamber()
            vt.port = self.port_test
            try:
                vt.open()  # in case of the climate chamber port is not open
            except:
                pass
            self.temperature = self.t_start
            self.temperature_storage = self.t_start  # a variable to store the start temperature
            vt.write(ON % self.temperature)  # ignite the climate chamber at the starting temperature
            [self.temp, self.temp2] = self.read(self.port_test)  # use the function reed to obtain the
            # temperature and the order of the climatic chamber
            while abs(self.temperature - self.t_end) >= abs(self.step_temp):
                self.value_mono_multi = 0
                self.write_doc("################################################")
                self.write_doc(f"Start of Test temperature {self.climate_chamber_num} : {self.temperature} degree "
                               f"Celsius")
                logger.debug("################################################")
                logger.debug(f"Start of Test temperature {self.climate_chamber_num}: {self.temperature} degree "
                             f"Celsius")
                vt.write(ON % self.temperature)
                self.wait_temperature_reach_consign()  # use the function wait_temperature_reach_consign to
                # reach and stabilize a the consigne
                self.temperature = self.temperature + self.step_temp  # The value of the temperature increase of
                # the step temperature value
                self.value = self.value_storage
                while self.value < 880000001:
                    self.change_value()
                    self.step_attenuate = 80
                    self.attenuate = 0
                    self.script()
                    if self.stopping == 1:
                        break
                    self.value += self.frequency_step
                self.temperature_storage += self.step_temp
                self.climate_chamber_num = self.climate_chamber_num + 1
            self.end_programme()
            vt.write(CLIMATIC_CHAMBER_STOP)
            sys.exit()
        else:
            while self.value < 880000001:
                self.change_value()
                self.step_attenuate = 80
                self.attenuate = 0
                self.script()
                if self.stopping == 1:
                    break
                self.value += self.frequency_step
            self.end_programme()
            sys.exit()

    def read_original_value(self):
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        cmd = file_execution(self.config_file, 7)
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        wah = stdout.readline()
        self.original_value = wah.split()

    def launch_climatic_chamber(self):  # settings menu of the IBTS
        new_window_climatic_chamber = Tk()
        new_window_climatic_chamber.title("climatic chamber settings")

        settings_frame = LabelFrame(new_window_climatic_chamber, text="Settings")
        settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        settings_frame.config(background='#fafafa')

        auto_stair_scale_frame = LabelFrame(settings_frame, bd=0)  # , text="auto_scale_frame"
        auto_stair_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
        auto_stair_scale_frame.config(background='#fafafa')

        start_auto_stair_scale_frame_button = Button(auto_stair_scale_frame, text="Start",
                                                     borderwidth=8, background=THE_COLOR,
                                                     activebackground="green", cursor="right_ptr",
                                                     overrelief="sunken",
                                                     command=lambda: [self.lunch_safety_climatic_chamber(
                                                         step_auto_stair_scale_frame_scale.get(),
                                                         temperature_start_stair_scale.get(),
                                                         temperature_end_auto_stair.get(),
                                                         time_temp_wait.get(),
                                                         new_window_climatic_chamber)])
        start_auto_stair_scale_frame_button.grid(row=0, column=0, ipadx=40, ipady=20, padx=0, pady=0)
        auto_stair_label = Label(auto_stair_scale_frame, text="The sensibility tests will take place during the "
                                                              "flat area", bg="white", font="arial",
                                 fg="black", relief="groove")
        auto_stair_label.grid(row=0, column=1, columnspan=4, ipadx=40, ipady=20, padx=0, pady=0)
        step_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='vertical', troughcolor=THE_COLOR,
                                                  from_=120, to=1,
                                                  resolution=1, tickinterval=20, length=100,
                                                  label='Step (°C)', state="active",
                                                  command=lambda x: [create_stair()])
        step_auto_stair_scale_frame_scale.grid(row=1, column=0, ipadx=10, ipady=10, padx=30, pady=0)
        step_auto_stair_scale_frame_scale.set(1)
        temperature_start_stair_scale = Scale(auto_stair_scale_frame, orient='vertical',
                                              troughcolor=THE_COLOR, from_=80, to=-40,
                                              resolution=1, tickinterval=20, length=100,
                                              command=lambda x: [create_stair()],
                                              label='Temperature start (°c)', state="active")
        temperature_start_stair_scale.grid(row=1, column=1, ipadx=10, ipady=10, padx=30, pady=0)
        temperature_start_stair_scale.set(-1)
        temperature_end_auto_stair = Scale(auto_stair_scale_frame, orient='vertical',
                                           troughcolor=THE_COLOR, from_=80, to=-40,
                                           resolution=1, tickinterval=20, length=100,
                                           command=lambda x: [create_stair()],
                                           label='Temperature end (°C)', state="active", relief="flat")
        temperature_end_auto_stair.grid(row=1, column=3, ipadx=10, ipady=10, padx=30, pady=0)
        temperature_end_auto_stair.set(1)

        def outdoor_settings():
            step_auto_stair_scale_frame_scale.set(20)
            temperature_start_stair_scale.set(-40)
            temperature_end_auto_stair.set(80)

        def indoor_settings():
            step_auto_stair_scale_frame_scale.set(20)
            temperature_start_stair_scale.set(0)
            temperature_end_auto_stair.set(55)

        outdoor_settings_radiobutton = Radiobutton(auto_stair_scale_frame, text="Outdoor settings",
                                                   variable=self.a, value=0, cursor="right_ptr",
                                                   indicatoron=0, command=lambda: [outdoor_settings()],
                                                   background=THE_COLOR,
                                                   activebackground="green",
                                                   bd=8, selectcolor="green", overrelief="sunken")
        outdoor_settings_radiobutton.grid(row=2, column=0, ipadx=10, ipady=10, padx=0, pady=0)
        indoor_settings_radiobutton = Radiobutton(auto_stair_scale_frame, text="Indoor settings",
                                                  variable=self.a, value=1, cursor="right_ptr",
                                                  indicatoron=0, command=lambda: [indoor_settings()],
                                                  background=THE_COLOR,
                                                  activebackground="green",
                                                  bd=8, selectcolor="green", overrelief="sunken")
        indoor_settings_radiobutton.grid(row=3, column=0, ipadx=10, ipady=10, padx=0, pady=0)
        indoor_settings_radiobutton.invoke()
        time_frame = LabelFrame(auto_stair_scale_frame, bd=0)  # , text="auto_scale_frame"
        time_frame.grid(row=4, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        time_frame.config(background='#fafafa')
        time_temp_wait_label = Label(time_frame, text="Time to wait at the temperature in minutes :")
        time_temp_wait_label.pack()
        time_temp_wait = Entry(time_frame, cursor="right_ptr")
        time_temp_wait.pack()
        time_temp_wait.insert(0, 2)

        def create_stair():
            simulation_graphic_stair(
                step_auto_stair_scale_frame_scale.get(),
                temperature_start_stair_scale.get(),
                temperature_end_auto_stair.get(),
                auto_stair_scale_frame)

        new_window_climatic_chamber.mainloop()

    def change_value(self):
        self.read_original_value()
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_izepto, username=username, password=password)
        cmd = file_execution(self.config_file, 9).split(",")
        order = (cmd[0] + str(self.original_value[1][:-1]) + cmd[2] + str(self.value) + cmd[4])
        ssh.exec_command(order, get_pty=True)

    def lunch_safety_climatic_chamber(self, step, t_start, t_end, time_temp_wait, window):  # a function to chek if all
        # the values are correct
        self.t_start = t_start
        self.t_end = t_end
        time_temp_wait = float(time_temp_wait)
        if time_temp_wait < 0 or time_temp_wait > 1000000:
            logger.critical("Error, The time wait value is not conform")
            showerror("Error", "The time wait value is not conform")
        else:
            if time_temp_wait == 0:
                time_temp_wait = 0.015
            self.time_temp_wait = (60 * time_temp_wait)
        if self.t_start == self.t_end:
            logger.critical("Error temperature_start = temperature_end")
        else:
            window.destroy()
            if self.t_start > self.t_end:
                self.step_temp = -step
            else:
                self.step_temp = step

    def name_files(self):
        a = []
        i = 0
        while sys.path[1].split('\\')[i] != 'automation-of-radio-frequency-tests':
            a.append(sys.path[1].split('\\')[i])
            i += 1
        for p in range(0, len(a)):
            self.file_path += str(a[p]) + '\\\\'
        self.file_path += 'automation-of-radio-frequency-tests\\\\Result_tests\\\\'

        if len(str(time.localtime()[1])) == 1:
            month = "0" + str(time.localtime()[1])
        else:
            month = str(time.localtime()[1])
        file_name = str(
            ("Data_filter_" + str(time.localtime()[2]) + "_" + month + "_" + str(time.localtime()[0]) + "_"
             + str(time.localtime()[3]) + str(time.localtime()[4]) + str(time.localtime()[5]) + ".txt"))
        self.data_file = self.file_path + file_name

        file_name_2 = str(
            ("Report_filter_" + str(time.localtime()[2]) + "_" + month + "_" + str(time.localtime()[0]) + "_"
             + str(time.localtime()[3]) + str(time.localtime()[4]) + str(time.localtime()[5]) + ".txt"))
        self.report_file = self.file_path + file_name_2

    def script(self):  # The script to test one channel
        for i in range(0, 100):  # number of test, generally infinity
            username = "root"
            password = "root"
            ssh = paramiko.SSHClient()  # initialisation de la liaison IBTS
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip_izepto, username=username, password=password)
            cmd = file_execution(self.config_file, 3) + "\n" + file_execution(self.config_file, 5)
            stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
            self.reponse_storage_izepto = []
            while 1:
                response = stdout.readline()
                self.reponse_storage_izepto.append(response + '\n')
                if response[0:5] == "ERROR":
                    self.number_error_izepto += 1
                    logger.critical("---------------------------------")
                    logger.critical("Failed to start the Izepto")
                    logger.critical("The Izepto is rebooting, please standby")
                    logger.critical("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc("Failed to start the Izepto")
                    self.write_doc("The Izepto is rebooting, please standby")
                    for e in range(0, len(self.reponse_storage_izepto)):
                        self.write_doc(self.reponse_storage_izepto[e])
                    self.write_doc("---------------------------------")
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
                        self.write_doc("The reboot is completed")
                        break
                if response[19:22] == "EUI":
                    logger.debug("The iZepto is ready")
                    self.number_launch += 1
                    break
            self.ready_ibts()
            #TODO Launch at the same time the initialisation
            # of the izepto and the ibts to take less time during the tests
            time.sleep(1)  # 1 second of safety after that the ready_ibts function is completed
            ssh.close()
            a = self.good_launch(stdout, i)
            if a == 1:
                if round(float(self.attenuate) / 4 + int(self.offset), 2) >= 126:
                    break
                self.attenuate = self.attenuate + self.step_attenuate
            else:
                number = round((len(a) / 4))
                result = (number / int(self.number_frames)) * 100
                if (round(result, 1) >= 90 and self.step_attenuate != 4) or self.step_attenuate == 1:
                    logger.debug("---------------------------------")
                    logger.debug(f"Test {i} of frequency {self.value} MHz")
                    logger.debug(
                        f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                    logger.debug(f"you send {self.number_frames} frames")
                    logger.debug(f"you received {number} frames")
                    logger.debug(f"The rate is : {round(result, 1)}%")
                    logger.debug("---------------------------------")

                    self.write_doc("---------------------------------")
                    self.write_doc(f"Test {i} of frequency {self.value} MHz")
                    self.write_doc(
                        f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                    self.write_doc(f"you send {self.number_frames} frames")
                    self.write_doc(f"you received {number} frames")
                    self.write_doc(f"The rate is : {round(result, 1)}%")
                    self.write_doc("---------------------------------")
                    self.write_data(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                                    self.power)
                    self.attenuate = self.attenuate + self.step_attenuate  # The value of the frequency_step
                    # increase of the step frequency_step value
                    if round(result, 1) == 0:
                        # self.window.destroy()
                        break

                elif round(result, 1) == 0 and self.attenuate == 0 and self.value < 867500000:
                    logger.debug("---------------------------------")
                    logger.debug(f"Test {i} of frequency {self.value} MHz")
                    logger.debug(f"The frequency {self.value} is too far away from the filter, stepping forward...")
                    logger.debug("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc(f"Test {i} of frequency {self.value} MHz")
                    self.write_doc(f"The frequency {self.value} is too far away from the filter, stepping forward...")
                    self.write_doc("---------------------------------")
                    break
                elif round(result, 1) == 0 and self.attenuate == 0 and self.value > 867500000:
                    logger.debug("---------------------------------")
                    logger.debug(f"Test {i} of frequency {self.value} MHz")
                    logger.debug(f"The frequency {self.value} is too far away from the filter, stopping...")
                    logger.debug("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc(f"Test {i} of frequency {self.value} MHz")
                    self.write_doc(f"The frequency {self.value} is too far away from the filter, stopping...")
                    self.write_doc("---------------------------------")
                    self.stopping = 1
                    break
                elif self.attenuate == 0 and round(result, 1) > 0:
                    self.step_attenuate = 1
                    logger.debug("---------------------------------")
                    logger.debug(f"Test {i} of frequency {self.value} MHz")
                    logger.debug(
                        f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                    logger.debug(f"you send {self.number_frames} frames")
                    logger.debug(f"you received {number} frames")
                    logger.debug(f"The rate is : {round(result, 1)}%")
                    logger.debug("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc(f"Test {i} of frequency {self.value} MHz")
                    self.write_doc(
                        f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                    self.write_doc(f"you send {self.number_frames} frames")
                    self.write_doc(f"you received {number} frames")
                    self.write_doc(f"The rate is : {round(result, 1)}%")
                    self.write_doc("---------------------------------")
                    self.write_data(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                                    self.power)
                elif self.step_attenuate == 4:
                    if round(result, 1) != 0:
                        logger.debug("---------------------------------")
                        logger.debug(f"Test {i} of frequency {self.value} MHz")
                        logger.debug(
                            f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                        logger.debug(f"you send {self.number_frames} frames")
                        logger.debug(f"you received {number} frames")
                        logger.debug(f"The rate is : {round(result, 1)}%")
                        logger.debug("---------------------------------")

                        self.write_doc("---------------------------------")
                        self.write_doc(f"Test {i} of frequency {self.value} MHz")
                        self.write_doc(
                            f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                        self.write_doc(f"you send {self.number_frames} frames")
                        self.write_doc(f"you received {number} frames")
                        self.write_doc(f"The rate is : {round(result, 1)}%")
                        self.write_doc("---------------------------------")
                        self.write_data(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                                        self.power)
                        self.attenuate = float(self.attenuate) + self.step_attenuate
                    else:
                        logger.debug("---------------------------------")
                        logger.debug(f"Test {i} of frequency {self.value} MHz")
                        logger.debug(f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB "
                                     f"is too "
                                     f"high, stepping back...")
                        logger.debug("---------------------------------")
                        self.write_doc("---------------------------------")
                        self.write_doc(f"Test {i} of frequency {self.value} MHz")
                        self.write_doc(
                            f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB is too high, "
                            f"stepping back...")
                        self.write_doc("---------------------------------")
                        self.attenuate = self.attenuate - self.step_attenuate
                        self.step_attenuate = 1
                        self.attenuate = self.attenuate + self.step_attenuate
                else:
                    logger.debug("---------------------------------")
                    logger.debug(f"Test {i} of frequency {self.value} MHz")
                    logger.debug(f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB is too "
                                 f"high, stepping back...")
                    logger.debug("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc(f"Test {i} of frequency {self.value} MHz")
                    self.write_doc(
                        f"The attenuation -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB is too high, "
                        f"stepping back...")
                    self.write_doc("---------------------------------")
                    self.attenuate = self.attenuate - self.step_attenuate
                    if self.step_attenuate == 80:
                        self.step_attenuate = 20
                    elif self.step_attenuate == 20:
                        self.step_attenuate = 4
                    elif self.step_attenuate == 4:
                        pass
                    self.attenuate = self.attenuate + self.step_attenuate
                    '''
                    if self.step_attenuate >= 20:
                        self.step_attenuate = self.step_attenuate / 2
                        self.attenuate = self.attenuate + self.step_attenuate
                    else:
                        self.step_attenuate = 4
                        self.attenuate = self.attenuate + self.step_attenuate
                    '''

    def good_launch(self, stdout, i):
        a = stdout.readlines()
        for d in range(0, len(a)):
            if a[d][0:5] == "ERROR":
                logger.critical("---------------------------------")
                logger.critical("Failed to receive correctly")
                logger.critical(f"Test {i} of frequency {self.value} MHz")
                logger.critical(f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                logger.critical("The Izepto is retrying")
                logger.critical("---------------------------------")
                self.write_doc("---------------------------------")
                self.write_doc("Failed to receive correctly")
                self.write_doc(f"Test {i} of frequency {self.value} MHz")
                self.write_doc(f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 2)} dB")
                self.write_doc("The Izepto is retrying")
                self.write_doc("---------------------------------")
                return 1
            else:
                d += 1
        return a

    def wait_temperature_reach_consign(self):
        while abs(self.temp - self.temperature) >= 0.2 or self.VALUE_STABILISATION <= self.time_temp_wait:
            # The maximal difference between the actual temperature and the order must be less than 0.2
            # (if we use a maximal difference of 0 it's take too much time to stabilize) AND the VALUE_STABILISATION
            # must be bigger than 120
            time.sleep(5)
            [self.temp, self.temp2] = self.read(self.port_test)  # Reed the value thanks to the reed function
            logger.info("#################################")  # show the values to the user
            logger.info(f"The actual temperature is : {self.temp}")
            logger.info(f"The actual order is : {self.temp2}")
            if abs(self.temp - self.temperature) < 0.2:  # If the maximal difference between the actual temperature
                # and the order is less than 0.2, launch the countdown.
                logger.info(f"The climate chamber is stabilized since {self.VALUE_STABILISATION} seconds of the "
                            f"{self.time_temp_wait} request")
                self.VALUE_STABILISATION = self.VALUE_STABILISATION + 5  # Because the loop cycle every 5 seconds, we
                # add 5 to the VALUE_STABILISATION
            else:  # If the maximal difference between the actual temperature and the order is 0.2 or more we
                # reset the VALUE_STABILISATION
                self.VALUE_STABILISATION = 0
        logger.info(f"The climate chamber is stabilized with success")
        logger.info("#################################")
        self.write_doc(f"The climate chamber is stabilized with success")
        self.write_doc("#################################")

    def read(self, the_port):
        try:  # This try allow the program to survive in a rare case where the climatic
            # chamber don't have enough time to answer back
            self.port_test = the_port
            vt.port = self.port_test
            try:
                vt.open()
            except:
                pass
            vt.write(b"$00I\n\r")  # prepare the climatic chamber to receive information
            time.sleep(0.2)  # A pause that freeze the entire program
            received_frame = vt.read_all().decode('utf-8')  # Decipher the frame that was send by the climatic
            # chamber
            word = received_frame.split(" ")  # Split the decipher the frame that was send by the climatic chamber
            strings = str(word[1])
            number = float(strings)  # Collect the actual temperature of the climatic chamber
            strings2 = str(word[0])
            number2 = strings2[-6:]
            number3 = float(number2)  # Collect the actual order of the climatic chamber
            return [number, number3]  # Return the actual temperature and the actual order at the same time to
            # allow the program to call read only once every 5 seconds, it's time saving (because of the time sleep)
        except:
            # logger.error("too fast, please wait")  # protect the application if the user
            # make a request the same time than the programme
            return [0, 0]  # In case of an error, this function will return [0,0], This will NOT affect the graph

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
            if frequency_step < 200000 or frequency_step > 100000000:
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
            if frequency < 851000000 or frequency > 950000000:
                logger.critical("Error, The frequency value is not conform")
                showerror("Error", "The frequency value is not conform")
            else:
                new_window_main_graphic.destroy()
                self.number_frames = number_frames
                self.value = frequency
                self.value_storage = frequency
                self.frequency_step = frequency_step
                self.sf = sf
                self.attenuate = attenuate
                self.offset = offset
                self.bw = bw
                self.power = power
        except:
            logger.critical("Error, One or more of the values are not conform")
            showerror("Error", "One or more of the values are not conform")

    def ready_ibts(self):  # initialise the IBTS
        #TODO Allow the modification of ibts attenuation "a la volé" without set up the
        # ibts at each test ("nx" command with x the attenuation)
        username = "root"
        password = "root"
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(hostname=self.ip_ibts, username=username, password=password)
        cmd = file_execution(self.config_file, 1).split(",")
        order = (cmd[0] + str(self.value / 1000000) + cmd[2] + str(self.bw) + cmd[4] + str(self.sf) + cmd[6] +
                 str(self.number_frames) + cmd[8] + str(abs(self.attenuate)))
        stdin, stdout, stderr = ssh2.exec_command(order, get_pty=True)
        self.reponse_storage_ibts = []
        while 1:
            read_value = stdout.readline()
            self.reponse_storage_ibts.append(read_value + '\n')
            if read_value[0:5] == "ERROR":
                logger.critical("---------------------------------")
                logger.critical("Failed to start the Ibts")
                logger.critical("The Ibts is rebooting, please standby")
                logger.critical("---------------------------------")
                self.write_doc("---------------------------------")
                self.write_doc("Failed to start the Ibts")
                self.write_doc("The Ibts is rebooting, please standby")
                for e in range(0, len(self.reponse_storage_ibts)):
                    self.write_doc(self.reponse_storage_ibts[e])
                self.write_doc("---------------------------------")
                ssh2.exec_command("reboot", get_pty=True)
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
                    self.write_doc(read_value)
                    if read_value[3:5] == "27":
                        logger.debug("The iBTS is ready")
                        break
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
        self.write_doc("End test")
        self.write_doc(f"Number of launch of the Izepto: {self.number_launch}")
        self.write_doc(f"Number of fail of the Izepto: {self.number_error_izepto}")
        self.write_doc(f'Test duration: {b[3] - 1}H{b[4]}min and {b[5]} second(s)')

    def write_doc(self, text):
        sensibility_result = open(self.report_file, 'a')
        sensibility_result.write(str(text) + "\n")
        sensibility_result.close()


def file_execution(file_name, n):
    a = []
    i = 0
    file_path = ''
    while sys.path[1].split('\\')[i] != 'automation-of-radio-frequency-tests':
        a.append(sys.path[1].split('\\')[i])
        i += 1
    for p in range(0, len(a)):
        file_path += str(a[p]) + '\\\\'
    file_path += 'automation-of-radio-frequency-tests\\\\Order_files\\\\'
    file_name = file_path + "Orders.txt"
    file = open(file_name, "r")
    donnees = []
    p = 0
    for line in file:
        donnees = donnees + line.rstrip('\n\r').split("=")
        p += 1
    file.close()
    return donnees[n]


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


def simulation_graphic_stair(step, temp_start, temp_end, window):  # create the simulation graph
    root = LabelFrame(window, bd=0)
    root.grid(column=1, row=2, columnspan=6, rowspan=4)
    my_draw_7_frame_2 = LabelFrame(root)
    my_draw_7_frame_2.pack()
    my_draw_7_frame_1 = LabelFrame(root)
    my_draw_7_frame_1.pack(side=BOTTOM)
    data = {0: 0}
    var = 0
    temp_duration = 2
    if temp_start == temp_end:
        for i in range(0, temp_duration):
            data[i] = temp_start
    else:
        if temp_end < temp_start:
            step = -step
        while abs(temp_start - temp_end) >= abs(step):
            for i in range(var, temp_duration + var):
                data[i] = temp_start
            var = var + temp_duration
            temp_start = temp_start + step
        for i in range(var, temp_duration + var):
            data[i] = temp_start
        if temp_start == temp_end:
            pass
        else:
            var = var + temp_duration
            for i in range(var, temp_duration + var):
                data[i] = temp_end

    names = list(data.keys())
    values = list(data.values())
    fig = Figure(figsize=(5, 3), dpi=100)
    fig.add_subplot().plot(names, values)
    fig.legend(["°C/hour"])
    canvas = FigureCanvasTkAgg(fig, master=my_draw_7_frame_1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
