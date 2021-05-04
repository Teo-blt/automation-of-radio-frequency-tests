#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 4 10:30:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# import
import serial  # requirment pyserial
import time
import threading
from tkinter import *
from tkinter.ttk import *

# =============================================================================

CLIMATIC_CHAMBER_STOP = b"$00E 0020.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
SET_TEMP_MIN = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SET_TEMP_MAX = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
VT = serial.Serial('COM11', SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
FIRST_TIME = False



class Mythread(threading.Thread):

    def __init__(self, temp_min, temp_max, temp_min_duration_h,
                 temp_max_duration_h, nb_cycle, oof, my_auto_scale_frame, type):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.temp_min = temp_min  # additional data added to the class
        self.temp_max = temp_max
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof
        self.root = my_auto_scale_frame
        self.type = type

    def run(self):
        if type == 1:
            VT.write(SET_TEMP_MIN % self.temp_min)
            p = 0
            while p < 1:
                print("start-up, please wait")
                time.sleep(2)
                print("start-up, please wait.")
                time.sleep(2)
                print("start-up, please wait..")
                time.sleep(2)
                print("start-up, please wait...")
                time.sleep(2)
                p = p + 1

            time_start = time.time()

            print("\n################################################\n")
            print("\nStart of Test\n")

            if self.oof:
                off()
            global i
            i = 0
            for i in range(0, self.nb_cycle):
                self.loop()
        else:
            print("deux")

    def loop(self):
        global FIRST_TIME, time_start_min
        VT.write(SET_TEMP_MIN % self.temp_min)
        time.sleep(0.5)
        print("the temperature is {}".format(read()))
        if self.read() > self.temp_min:
            self.root.after(500, self.loop)  # => loop after 0.5 seconde
        else:
            if not FIRST_TIME:
                time_start_min = time.time()
                FIRST_TIME = True

            print(time.time())
            print(time_start_min + (60))
            if time.time() < time_start_min + (60):  # self.temp_min_duration_h * 3600
                self.root.after(500, self.loop)  # => loop after 0.5 seconde
            else:
                self.exit()

    def off(self):
        try:
            VT.write(CLIMATIC_CHAMBER_STOP)
        except:
            print("Error, the climate chamber is already offline")

    def exit(self):
        global i
        print(f'End of cycle {i}: {time.time() - time_start}\n')
        # Stop climatic chamber
        self.off()
        time_stop = time.time()
        print("\n################################################\n")
        print("\nEnd of Test\n")
        print(f'Test duration: {time_stop - time_start}\n')


    def read(self):
        VT.write(b"$00I\n\r")
        time.sleep(0.5)
        received_frame = VT.read_all().decode('utf-8')
        word = received_frame.split(" ")
        strings = str(word[1])
        number = float(strings)
        return number
