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
import time
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from loguru import logger
import serial

# =============================================================================
THE_COLOR = "#E76145"
CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
vt = serial.Serial()


class Threadsensibility(threading.Thread):

    def __init__(self, ip_address, ip, port_test, window):
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
        self.step_attenuate = 0
        self.offset = 0
        self.test = 0
        self.bw = 0
        self.step_temp = 0
        self.t_start = 0
        self.t_end = 0
        self.temperature = 0
        self.temp = 0
        self.temp2 = 0
        self.VALUE_STABILISATION = 0
        self.power = 0
        self.a = 0
        self.window = window
        self.climate_chamber_num = 0
        self.b = 0
        self.value_mono_multi = 0
        self.attenuate_storage = 0
        self.frequency_entry = tk.Entry
        self.name_file = 'test.txt'
        self.frequency_storage = 0
        self.number_channel = 8
        self.time_temp_wait = 120
        self.temperature_storage = 0

    def run(self):
        sensibility_result = open("Report_sensibility.txt", 'w+')
        sensibility_result.close()
        outfile = open(self.name_file, 'w+')
        outfile.close()
        self.write_doc("Sensitivity measurement iZepto")
        self.write_doc("Sensitivity measurement iBTS")
        self.launch_ibts()
        if self.value_mono_multi:
            if self.port_test != -1:
                self.launch_climatic_chamber()
                vt.port = self.port_test
                try:
                    vt.open()
                except:
                    pass
                self.temperature = self.t_start
                self.temperature_storage = self.t_start
                vt.write(ON % self.temperature)
                [self.temp, self.temp2] = self.read(self.port_test)
                while abs(self.temperature - self.t_end) >= abs(self.step_temp):
                    self.value_mono_multi = 0
                    self.frequency = self.frequency_storage
                    self.write_doc("################################################")
                    self.write_doc(f"Start of Test temperature {self.climate_chamber_num} : {self.temperature} degree "
                                   f"Celsius")
                    logger.debug("################################################")
                    logger.debug(f"Start of Test temperature {self.climate_chamber_num}: {self.temperature} degree "
                                 f"Celsius")
                    vt.write(ON % self.temperature)
                    self.wait_temperature_reach_consign()
                    self.temperature = self.temperature + self.step_temp
                    for p in range(0, self.number_channel):
                        logger.debug(
                            f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}, frequency: {round(self.frequency, 1)}")
                        self.write_doc(f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}"
                                       f", frequency: "
                                       f"{round(self.frequency, 1)}")
                        self.script()
                        self.frequency = self.frequency + 0.2
                        self.value_mono_multi = self.value_mono_multi + 1
                    logger.debug(f"fin test")
                    self.write_doc(f"fin test")
                    self.climate_chamber_num = self.climate_chamber_num + 1
                for u in range(0, 2):
                    if u != 0:
                        self.temperature = self.t_end
                    self.value_mono_multi = 0
                    self.write_doc(f"Start of Test temperature {self.climate_chamber_num}")
                    self.write_doc("Start of Test")
                    logger.debug("################################################")
                    logger.debug(f"Start of Test temperature {self.climate_chamber_num}")
                    self.frequency = self.frequency_storage
                    self.temperature = self.t_end
                    vt.write(ON % self.temperature)
                    self.wait_temperature_reach_consign()
                    for p in range(0, self.number_channel):
                        logger.debug(
                            f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}, frequency:"
                            f" {round(self.frequency, 1)}")
                        self.write_doc(f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}, frequency: "
                                       f"{round(self.frequency, 1)}")
                        self.script()
                        self.frequency = self.frequency + 0.2
                        self.value_mono_multi = self.value_mono_multi + 1
                logger.debug("End test climatic chamber")
                vt.write(CLIMATIC_CHAMBER_STOP)
            else:
                self.value_mono_multi = 0
                for p in range(0, self.number_channel):
                    logger.debug(f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}, "
                                 f"frequency: {round(self.frequency, 1)}")
                    self.write_doc(f"Channel number: {self.value_mono_multi} of {self.number_channel - 1}, frequency: "
                                   f"{round(self.frequency, 1)}")
                    self.attenuate = self.attenuate_storage
                    self.script()
                    self.frequency = self.frequency + 0.2
                    self.value_mono_multi = self.value_mono_multi + 1
                logger.debug(f"fin test")
                self.write_doc(f"fin test")
        else:
            if self.port_test != -1:
                self.climate_chamber_script()
            else:
                self.script()

    def climate_chamber_script(self):
        self.launch_climatic_chamber()
        vt.port = self.port_test
        try:
            vt.open()
        except:
            pass
        self.temperature = self.t_start
        vt.write(ON % self.temperature)
        [self.temp, self.temp2] = self.read(self.port_test)
        while abs(self.temperature - self.t_end) >= abs(self.step_temp):
            self.write_doc(f"Start of Test temperature {self.climate_chamber_num}")
            self.write_doc("Start of Test")
            logger.debug("################################################")
            logger.debug(f"Start of Test temperature {self.climate_chamber_num}")
            vt.write(ON % self.temperature)
            self.wait_temperature_reach_consign()
            self.script()
            self.temperature = self.temperature + self.step_temp
            self.climate_chamber_num = self.climate_chamber_num + 1
        self.write_doc(f"Start of Test temperature {self.climate_chamber_num}")
        self.write_doc("Start of Test")
        logger.debug("################################################")
        logger.debug(f"Start of Test temperature {self.climate_chamber_num}")
        self.temperature = self.t_end
        vt.write(ON % self.temperature)
        self.wait_temperature_reach_consign()
        self.script()
        vt.write(CLIMATIC_CHAMBER_STOP)

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
        self.write_doc(f"The climate chamber is stabilized with success")

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
            # TODO find a better way to wait maybe asyncio.sleep(5) ?
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

    def script(self):
        for i in range(0, int(self.test)):
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
                if wah[0:5] == "ERROR":
                    logger.critical("---------------------------------")
                    logger.critical("Failed to start the concentrator")
                    logger.critical("The Izepto is rebooting, please standby")
                    logger.critical("---------------------------------")
                    self.write_doc("---------------------------------")
                    self.write_doc("Failed to start the concentrator")
                    self.write_doc("The Izepto is rebooting, please standby")
                    self.write_doc("---------------------------------")
                    ssh.exec_command("reboot", get_pty=True)
                    for t in range(0, 10):
                        logger.info("Izepto rebooting, it may take few minutes")
                        time.sleep(5)
                    username = "root"
                    password = "root"
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.ip, username=username, password=password)
                    cmd = "./lora_pkt_fwd -c global_conf.json.sx1250.EU868"
                    cmd2 = "cd /user/libsx1302-utils_V1.0.5-klk1-dirty"
                    stdin, stdout, stderr = ssh.exec_command(cmd2 + "\n" + cmd, get_pty=True)
                    if wah[19:22] == "EUI":
                        logger.debug("The iZepto is ready")
                        logger.debug("The reboot is completed")
                        self.write_doc("The reboot is completed")
                        break
                if wah[19:22] == "EUI":
                    logger.debug("The iZepto is ready")
                    break
            if i == 0:
                self.attenuate = self.attenuate_storage
                self.ready_ibts()
            else:
                self.attenuate = float(self.attenuate) + self.step_attenuate
                self.ready_ibts()
            time.sleep(1)
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

            self.write_doc("---------------------------------")
            if int(self.test) == 1000:
                self.write_doc(f"Test {i} of inf of channel number: {self.value_mono_multi}")
            else:
                self.write_doc(f"Test {i} of {self.test}")
            self.write_doc(
                f"The level of attenuation is : -{round(float(self.attenuate) / 4 + int(self.offset), 1)} dB")
            self.write_doc(f"you send {self.number_frames} frames")
            self.write_doc(f"you received {number} frames")
            self.write_doc(f"The rate is : {round(result, 1)}%")
            self.write_doc("---------------------------------")
            self.write_json(round(float(self.attenuate) / 4 + int(self.offset), 2), 100 - round(result, 2),
                            self.power)
            self.temperature_storage += self.step_temp
            if round(result, 1) == 0:
                logger.debug(f"fin channel number: {self.value_mono_multi}\n")
                self.write_doc(f"fin channel number: {self.value_mono_multi}\n")
                # self.window.destroy()
                break

    def launch_climatic_chamber(self):
        new_window_climatic_chamber = Tk()
        new_window_climatic_chamber.title("climatic chamber settings")

        settings_frame = LabelFrame(new_window_climatic_chamber, text="Settings")
        settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        settings_frame.config(background='#fafafa')

        auto_stair_scale_frame = LabelFrame(settings_frame, bd=0)  # , text="auto_scale_frame"
        auto_stair_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
        auto_stair_scale_frame.config(background='#fafafa')

        start_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Start",
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
        auto_stair_label = tk.Label(auto_stair_scale_frame, text="The sensibility tests will take place during the "
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

        outdoor_settings_radiobutton = tk.Radiobutton(auto_stair_scale_frame, text="Outdoor settings",
                                                      variable=self.a, value=0, cursor="right_ptr",
                                                      indicatoron=0, command=lambda: [outdoor_settings()],
                                                      background=THE_COLOR,
                                                      activebackground="green",
                                                      bd=8, selectcolor="green", overrelief="sunken")
        outdoor_settings_radiobutton.grid(row=2, column=0, ipadx=10, ipady=10, padx=0, pady=0)
        indoor_settings_radiobutton = tk.Radiobutton(auto_stair_scale_frame, text="Indoor settings",
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

    def lunch_safety_climatic_chamber(self, step, t_start, t_end, time_temp_wait, window):
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

    def value_change(self, a):
        self.value_mono_multi = a
        if a:
            self.frequency_entry.delete(0, 20)
            self.frequency_entry.insert(0, 867100000)
            self.frequency_entry.config(state='readonly')
        else:
            self.frequency_entry.config(state='normal')

    def launch_ibts(self):
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
        channel_mono_radiobutton = tk.Radiobutton(packet_frame, text="Mono channel",
                                                  variable=self.b, value=0, cursor="right_ptr",
                                                  indicatoron=0, command=lambda: [self.value_change(0)],
                                                  background=THE_COLOR,
                                                  activebackground="green",
                                                  bd=8, selectcolor="green", overrelief="sunken")
        channel_mono_radiobutton.grid(row=4, column=0, ipadx=10, ipady=10, padx=0, pady=0)
        channel_multi_radiobutton = tk.Radiobutton(packet_frame, text="Multi channel",
                                                   variable=self.b, value=1, cursor="right_ptr",
                                                   indicatoron=0, command=lambda: [self.value_change(1)],
                                                   background=THE_COLOR,
                                                   activebackground="green",
                                                   bd=8, selectcolor="green", overrelief="sunken")
        channel_multi_radiobutton.grid(row=4, column=1, ipadx=10, ipady=10, padx=0, pady=0)
        channel_mono_radiobutton.invoke()

        reset_button = tk.Button(scale_frame, text="Reset",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.reset_all(self.frequency_entry, sf, attenuate,
                                                                 number_frames, step, offset, test, bw)])
        reset_button.pack(padx=0, pady=0, expand=True, fill="both", side=BOTTOM)

        start_button = tk.Button(scale_frame, text="Start",
                                 borderwidth=8, background=THE_COLOR,
                                 activebackground="green", cursor="right_ptr", overrelief="sunken",
                                 command=lambda: [self.lunch_safety_ibts(self.frequency_entry, sf, attenuate,
                                                                         number_frames,
                                                                         step, offset, test, bw, power,
                                                                         new_window_ibts)])
        start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
        new_window_ibts.mainloop()

    def lunch_safety_ibts(self, frequency, sf, attenuate, number_frames, step, offset, test, bw, power,
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

    def write_doc(self, text):
        sensibility_result = open("Report_sensibility.txt", 'a')
        sensibility_result.write(str(text) + "\n")
        sensibility_result.close()

    def write_json(self, attenuation_db, packet_lost, power_out):
        outfile = open(self.name_file, 'a')
        power_in = round(power_out - attenuation_db, 2)
        outfile.write(str(power_in) + ' ' + str(round(packet_lost)) + ' ' + str(self.climate_chamber_num)
                      + ' ' + str(self.value_mono_multi) + ' ' + str(self.temperature_storage) + '\n')
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


def simulation_graphic_stair(step, temp_start, temp_end, window):
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
