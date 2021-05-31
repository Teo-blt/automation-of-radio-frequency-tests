#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 25 16:04:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import pyvisa as visa
import serial
import os
import time
import sys
import threading
from tkinter import *
import tkinter as tk
from loguru import logger

# =============================================================================
THE_COLOR = "#E76145"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5


def lunch_smiq(gpib_port, type_gpib):
    new_window_main_graphic = tk.Toplevel()
    new_window_main_graphic.title("Signal generator settings")

    settings_frame = LabelFrame(new_window_main_graphic, text="Settings")
    settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    settings_frame.config(background='#fafafa')

    scale_frame = LabelFrame(settings_frame, bd=0)  # , text="Scales"
    scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_frame.config(background='#fafafa')

    delay_scale = Scale(scale_frame, orient='vertical', troughcolor=THE_COLOR, from_=1, to=10,
                        resolution=1, tickinterval=2, length=100,
                        label='Delay between measurement (s)', state="active")
    delay_scale.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)

    frames_nb_scale = Scale(scale_frame, orient='vertical', troughcolor=THE_COLOR, from_=1, to=10,
                            resolution=1, tickinterval=2, length=100,
                            label='Number of sent frames', state="active")
    frames_nb_scale.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    """
    entry_frame = LabelFrame(scale_frame, text="Entry settings")
    entry_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    Entry_label = Label(entry_frame, text="List of Measurement channel (Hz) :")
    Entry_label.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    measurement_channel = Entry(entry_frame, cursor="right_ptr")
    measurement_channel.pack(padx=0, pady=0, side=LEFT)
    measurement_channel.insert(0, 868950000)
    reset_button = tk.Button(entry_frame, text="Reset",
                             borderwidth=8, background=THE_COLOR,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [measurement_channel.delete(0, 20),
                                              measurement_channel.insert(0, 868950000)])
    reset_button.pack(expand=False, fill="none", side=RIGHT)
    """
    start_button = tk.Button(scale_frame, text="Start",
                             borderwidth=8, background=THE_COLOR,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [
                                 Threadsmiq(delay_scale.get(), frames_nb_scale.get(), gpib_port, type_gpib).start()])
    start_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    off_scale_frame_button = tk.Button(scale_frame, text="Off",
                                       borderwidth=8, background=THE_COLOR,
                                       activebackground="green", cursor="right_ptr", overrelief="sunken",
                                       command=lambda: [])
    off_scale_frame_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)


class Threadsmiq(threading.Thread):

    def __init__(self, nb_frame, wait_measure, gpib_port, type_gpib):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.nb_frame = nb_frame  # Number of sent frames
        self.wait_measure = wait_measure  # Delay between measurement (s)
        self.channel_list = [868950000]  # List of Measurement channel (Hz)
        self.coupler_attent_send_to_EUT = 0
        self.gpib_port = gpib_port
        self.type_gpib = type_gpib

    def run(self):
        sys.path.append('P:\\e2b\\hardware\\Scripts_auto\\Python\\lib')
        rm = visa.ResourceManager()
        smiq_send = rm.open_resource(self.type_gpib + '::' + self.gpib_port + '::INSTR')
        smiq_send.write('*RST')
        logger.info(smiq_send.query('*IDN?'))
        smiq_send.write('OUTP:STAT OFF')  # RF Output OFF
        smiq_send.write('SOUR:DM:STAT ON')  # Digital Modulation ON
        smiq_send.write('SOUR:DM:SOUR DLIST')  # Source selection
        smiq_send.write("SOUR:DM:DLIST:SEL 'T1_TEST'")  # 169_N2
        smiq_send.write('SOUR:DM:SEQ SINGLE')  # AUTO | RETRigger | AAUTo | ARETrigger | SINGle
        # Rectangle filter mandatory for WM4800 !
        smiq_send.write('SOUR:DM:FILT:TYPE RECT')
        # SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 | EIS95 | APCO |
        # TETRa | WCDMa | RECTangle | SPHase | USER

        mod_list = [  # Modulation, BW or Dev, SF or Bitrate, OBW, Sensitivity_level
            ['G', 45000, 100000, 250000, -110],  # Real sensitivity = -121 / Theoretical sensitivity = -109 (7kHz RxBW)
            # ['L',7.8,341,12500, -137] #Real sensitivity = -137 / Theoretical sensitivity = -108 (7.8kHz RxBW)
        ]
        rssi_average = -999

        # Result folder
        result_path = "C:/Users/labo/PycharmProjects/automation-of-radio-frequency-tests/SMIQ"
        result_path += '\\Sensi'

        ################################################
        # Devices
        """
        serial_speed = 115200
        serial_timeout = 5
        DUT = serial.Serial('COM13', serial_speed, timeout=serial_timeout)
        """
        ################################################################################################
        # MEASUREMENT Loop
        ################################################################################################
        logger.info("################################################")
        logger.info("Start of Test")
        time_start = time.time()
        for mod in mod_list:

            freq_dev = mod[1]
            bitrate = mod[2]
            sensitivity_level = mod[4]

            csv_result = open("test_smiq", 'w+')
            csv_result.write("Sensitivity measurement\n")
            csv_result.write("EN300 220-1 v3.1.1\n")
            csv_result.write("Time; Channel frequency; Signal Level; Nb frame sent; PER\n\n")

            for freq in self.channel_list:

                # Configure sending device modulation
                smiq_send.write('SOUR:DM:FORM FSK2')  # FSK2 / GFSK
                smiq_send.write('SOUR:DM:SRATe %d Hz' % bitrate)  # symbol rate 1kHz to 7 MHz /
                # Set rate BEFORE deviation
                smiq_send.write('SOUR:DM:FSK:DEV %d' % freq_dev)  # frequency deviation 100 Hz to 2.5 MHz
                smiq_send.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
                smiq_send.write('SOUR:FREQ:CW %d' % freq)  # Set channel frequency
                # smiq_send.write('SOUR:DM:FILT:TYPE RECTangle')
                # SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 |
                # EIS95 | APCO | TETRa | WCDMa | RECTangle | SPHase | USER

                smiq_send.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
                smiq_send.write('OUTP:STAT ON')  # RF Output ON

                smiq_send.write('SOUR:POW:MODE FIX')  # Set power to "Fixed" mode

                sensitivity_steps = list(range(sensitivity_level - 4, sensitivity_level + 11, 1))
                sensitivity_steps = sensitivity_steps + list(range(sensitivity_level + 11, sensitivity_level + 21, 2))
                sensitivity_steps = sensitivity_steps + list(
                    range(round((sensitivity_level + 26) / 10) * 10, 0, 10))  # Round to the upper decade
                logger.info(f'Power levels steps calculated: {sensitivity_steps}')

                for signal_level in sensitivity_steps:

                    smiq_send.write('POW %d' % (
                            signal_level + self.coupler_attent_send_to_EUT))
                    # Set output power level at Theoretical sensitivity + 3dB

                    # Set product in reception
                    # DUT.write(b"\n")
                    # DUT.write(b"startrx %d %d \n" % (mode, channel_number))
                    # time.sleep(1)

                    nb_frame_sent = 0
                    nb_frame_received = 0
                    logger.info(f'Sending {self.nb_frame} frames at {signal_level}dBm...')
                    for i in range(0, self.nb_frame):
                        # Send 1 frame
                        logger.info('===========')
                        logger.info(f' Sending frame {i + 1}/{self.nb_frame}...')
                        smiq_send.write('TRIG:DM:IMM')  # Send 1 trigger event
                        nb_frame_sent = nb_frame_sent + 1
                        time.sleep(1)
                        # Check frame reception
                        # received_frame = DUT.read_all().decode('utf-8')

                        # ToDo Add RSSI recording
                        """
                        print(received_frame)
                        if str_received_address_check in received_frame:
                            print(f'Frame {i + 1}/{nb_frame} received !')
                            nb_frame_received = nb_frame_received + 1
                            rssi.append(int(received_frame[received_frame.find('RSSI') + 5:received_frame.find(',')]))
                        
                    if nb_frame_received > 0:
                        rssi_average = sum(rssi) / len(rssi)
                    """
                    time.sleep(1)
                    logger.info("DUT read")
                    # print(DUT.read_all().decode('utf-8'))

                    per = (nb_frame_sent - nb_frame_received) / nb_frame_sent
                    logger.info(f'Frame sent = {nb_frame_sent}')
                    logger.info(f'PER = {per}')

                    # Time; Channel frequency; Signal Level; Nb frame sent; PER ; RSSI
                    res_str = f'Date : {time.asctime()}\nFrequency : {freq}Hz;\nSignal level : {signal_level}dBm;' \
                              f'\nNumber of frames sent : {nb_frame_sent};\nPercentage of loose {per * 100}%;' \
                              f'\nRssi average : {rssi_average}\n\n'
                    logger.info(f'Date : {time.asctime()}')
                    logger.info(f'Frequency : {freq}Hz')
                    logger.info(f'Signal level : {signal_level}dBm')
                    logger.info(f'Number of frames sent : {nb_frame_sent}')
                    logger.info(f'Percentage of loose {per * 100}%')
                    logger.info(f'Rssi average : {rssi_average}')
                    csv_result.write(res_str)

                    time.sleep(self.wait_measure)

            csv_result.close()

        time_stop = time.time()
        logger.info("################################################")
        logger.info("End of Test")
        a = time.localtime(time_stop - time_start)
        logger.info(f'Test duration : {a[3] - 1}H{a[4]} and {a[5]} second(s)')
        # DUT.close()
