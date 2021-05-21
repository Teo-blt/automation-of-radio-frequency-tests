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
# =============================================================================
class Thread_smiq(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class


    def run(self):
        sys.path.append('P:\\e2b\\hardware\\Scripts_auto\\Python\\lib')
        rm = visa.ResourceManager()
        SMIQ_SEND = rm.open_resource('GPIB0::28::INSTR')
        SMIQ_SEND.write('*RST')
        print(SMIQ_SEND.query('*IDN?'))
        SMIQ_SEND.write('OUTP:STAT OFF')  # RF Output OFF
        SMIQ_SEND.write('SOUR:DM:STAT ON')  # Digital Modulation ON
        SMIQ_SEND.write('SOUR:DM:SOUR DLIST')  # Source selection
        SMIQ_SEND.write("SOUR:DM:DLIST:SEL 'T1_TEST'")  # 169_N2
        SMIQ_SEND.write('SOUR:DM:SEQ SINGLE')  # AUTO | RETRigger | AAUTo | ARETrigger | SINGle
        # Rectangle filter mandatory for WM4800 !
        SMIQ_SEND.write('SOUR:DM:FILT:TYPE RECT')
        # SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 | EIS95 | APCO | TETRa | WCDMa | RECTangle | SPHase | USER

        nb_frame = 1  # Number of sent frames
        wait_measure = 1  # Delay between measurement (s)
        coupler_atten_send_to_EUT = 0

        channel_list = [  # List of Measurement channel (Hz), channel number
            868950000
        ]

        mod_list = [  # Modulation, BW or Dev, SF or Bitrate, OBW, Sensitivity_level
            ['G', 45000, 100000, 250000, -110],  # Real sensitivity = -121 / Theoretical sensitivity = -109 (7kHz RxBW)
            # ['L',7.8,341,12500, -137] #Real sensitivity = -137 / Theoretical sensitivity = -108 (7.8kHz RxBW)
        ]

        str_received_address_check = "CEN-785634120107"
        str_received_payload_check = "PAYLOAD (19) = \n\rb4 f0 e1 d2 c3 b4 a5 96 87 78 69 5a 4b 3c 2d 1e \n\r0f 55 ff"
        rssi = []
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

        print("################################################")
        print("Start of Test")
        time_start = time.time()
        for mod in mod_list:
            modulation = mod[0].encode('utf-8')
            freq_dev = mod[1]
            bitrate = mod[2]
            OCW = mod[3]
            sensitivity_level = mod[4]

            seq_time = time.localtime()
            filename = "test_smiq"

            csv_result = open(filename, 'w+')
            csv_result.write("Sensitivity measurement\n")
            csv_result.write("EN300 220-1 v3.1.1\n")
            csv_result.write("Time; Channel frequency; Signal Level; Nb frame sent; PER\n\n")

            for freq in channel_list:

                # Configure sending device modulation
                SMIQ_SEND.write('SOUR:DM:FORM FSK2')  # FSK2 / GFSK
                SMIQ_SEND.write('SOUR:DM:SRATe %d Hz' % bitrate)  # symbol rate 1kHz to 7 MHz / Set rate BEFORE deviation
                SMIQ_SEND.write('SOUR:DM:FSK:DEV %d' % freq_dev)  # frequency deviation 100 Hz to 2.5 MHz
                SMIQ_SEND.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
                SMIQ_SEND.write('SOUR:FREQ:CW %d' % freq)  # Set channel frequency
                # SMIQ_SEND.write('SOUR:DM:FILT:TYPE RECTangle')
                # SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 |
                # EIS95 | APCO | TETRa | WCDMa | RECTangle | SPHase | USER

                SMIQ_SEND.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
                SMIQ_SEND.write('OUTP:STAT ON')  # RF Output ON

                SMIQ_SEND.write('SOUR:POW:MODE FIX')  # Set power to "Fixed" mode

                sensitivity_steps = list(range(sensitivity_level - 4, sensitivity_level + 11, 1))
                sensitivity_steps = sensitivity_steps + list(range(sensitivity_level + 11, sensitivity_level + 21, 2))
                sensitivity_steps = sensitivity_steps + list(
                    range(round((sensitivity_level + 26) / 10) * 10, 0, 10))  # Round to the upper decade
                print(f'\nPower levels steps calculated: {sensitivity_steps}')

                for signal_level in sensitivity_steps:

                    SMIQ_SEND.write('POW %d' % (
                            signal_level + coupler_atten_send_to_EUT))
                    # Set output power level at Theoretical sensitivity + 3dB

                    # Set product in reception
                    # DUT.write(b"\n")
                    # DUT.write(b"startrx %d %d \n" % (mode, channel_number))
                    # time.sleep(1)

                    nb_frame_sent = 0
                    nb_frame_received = 0
                    print(f'Sending {nb_frame} frames at {signal_level}dBm...')
                    for i in range(0, nb_frame):

                        # Send 1 frame
                        print(f'\n==========\nSending frame {i + 1}/{nb_frame}...')
                        SMIQ_SEND.write('TRIG:DM:IMM')  # Send 1 trigger event
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
                    print("DUT read")
                    #print(DUT.read_all().decode('utf-8'))

                    PER = (nb_frame_sent - nb_frame_received) / nb_frame_sent
                    print(f'\nFrame sent = {nb_frame_sent}')
                    print(f'PER = {PER}')

                    # Time; Channel frequency; Signal Level; Nb frame sent; PER ; RSSI
                    res_str = f'Date : {time.asctime()}\nFrequency : {freq}Hz;\nSignal level : {signal_level}dBm;' \
                              f'\nNumber of frames sent : {nb_frame_sent};\nPercentage of loose {PER * 100}%;' \
                              f'\nRssi average : {rssi_average}\n\n'
                    print(res_str)
                    csv_result.write(res_str)

                    time.sleep(wait_measure)

            csv_result.close()

        time_stop = time.time()
        print("################################################")
        print("End of Test")
        a = time.localtime(time_stop - time_start)
        print(f'Test duration : {a[3]}H{a[4]} and {a[5]} second(s)')
        #DUT.close()


