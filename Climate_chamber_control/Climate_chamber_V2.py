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

# =============================================================================

CLIMATIC_CHAMBER_STOP = b"$00E 0020.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
CONNECTION = 'COM11'
try :
    VT = serial.Serial(CONNECTION, SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
except :
    print("impossible connection")
FIRST_TIME = False


class Mythread(threading.Thread):

    def __init__(self, temp_min, temp_max, temp_min_duration_h,
                 temp_max_duration_h, nb_cycle, oof, my_auto_scale_frame):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.temp_min = temp_min  # additional data added to the class
        self.temp_max = temp_max
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof
        self.root = my_auto_scale_frame

    def run(self):
        VT.write(ON % self.temp_min)
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
            self.off()
        global i
        i = 0
        for i in range(0, self.nb_cycle):
            self.loop(time_start)

    def loop(self, time_start):
        global FIRST_TIME, time_start_min
        VT.write(ON % self.temp_min)
        time.sleep(0.5)
        print("the temperature is {}".format(self.read()))
        if self.read()[1] > self.temp_min:
            self.root.after(500, self.loop)  # => loop after 0.5 seconde
        else:
            if not FIRST_TIME:
                time_start_min = time.time()
                FIRST_TIME = True

            print(time.time())
            print(time_start_min + (self.temp_min_duration_h * 3600))
            if time.time() < time_start_min + (self.temp_min_duration_h * 3600):
                self.root.after(500, self.loop)  # => loop after 0.5 seconde
            else:
                self.exit(time_start)

    def off(self):
        try:
            VT.write(CLIMATIC_CHAMBER_STOP)
        except:
            print("Error, the climate chamber is already offline")

    def exit(self, time_start):
        global i
        print(f'End of cycle {i}: {time.time() - time_start}\n')
        # Stop climatic chamber
        self.off()
        time_stop = time.time()
        print("\n################################################\n")
        print("\nEnd of Test\n")
        print(f'Test duration: {time_stop - time_start}\n')

    def read(self):
        try :
            VT.write(b"$00I\n\r")
            time.sleep(0.5)
            received_frame = VT.read_all().decode('utf-8')
            word = received_frame.split(" ")
            strings = str(word[1])
            number = float(strings)
            strings2 = str(word[0])
            number2 = float(strings2)
            return [number, number2]
        except:
            print("error, it's too early")

    def order(self, value):
        print("The new order value is : {}".format(value.get()))
        VT.write(ON % value.get())







