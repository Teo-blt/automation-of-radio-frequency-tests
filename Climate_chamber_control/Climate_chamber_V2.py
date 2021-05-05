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
FIRST_TIME = False
VALUE_STABILISATION = 0

try:
    VT = serial.Serial(CONNECTION, SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
except:
    print("impossible connection")


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
        while p < 0:
            print("start-up, please wait")
            time.sleep(2)
            print("start-up, please wait.")
            time.sleep(2)
            print("start-up, please wait..")
            time.sleep(2)
            print("start-up, please wait...")
            time.sleep(2)
            p = p + 1

        global time_start
        time_start = time.time()

        print("\n################################################\n")
        print("\nStart of Test\n")

        if self.oof:
            self.off()

        global i
        i = 0

        VT.write(ON % self.temp_min)

        for i in range(0, self.nb_cycle):
            self.loop(FIRST_TIME, VALUE_STABILISATION)

    def loop(self, FIRST_TIME, VALUE_STABILISATION):
        global time_start_min
        temp = self.read()[1]
        temp2 = self.read()[0]
        print("#################################")
        print("The actual themperature is : {}".format(temp2))
        print("The actual order is : {}".format(temp))
        if temp2 != self.temp_min:
            VALUE_STABILISATION = 0
            self.root.after(5000, self.loop(FIRST_TIME, VALUE_STABILISATION))  # => loop after 5 secondes
        elif temp2 == self.temp_min:
            if VALUE_STABILISATION < 25:
                VALUE_STABILISATION = VALUE_STABILISATION + 1
                print("p vaut {}".format(VALUE_STABILISATION))
                self.root.after(5000, self.loop(FIRST_TIME, VALUE_STABILISATION))
            else:
                if not FIRST_TIME:
                    time_start_min = time.time()
                    FIRST_TIME = True
                print(time.time())
                print(time_start_min + (60)) # self.temp_min_duration_h * 3600)
                if time.time() < time_start_min + (60):
                    self.root.after(5000, self.loop(FIRST_TIME, VALUE_STABILISATION))  # => loop after 5 secondes
                else:
                    self.exit()

    def off(self):
        try:
            VT.write(CLIMATIC_CHAMBER_STOP)
        except:
            print("Error, the climate chamber is already offline")

    def exit(self):
        global i
        global time_start
        print(f'End of cycle {i}: {time.time() - time_start}\n')
        # Stop climatic chamber
        self.off()
        time_stop = time.time()
        print("\n################################################\n")
        print("\nEnd of Test\n")
        print(f'Test duration: {time_stop - time_start}\n')

    def read(self):
        VT.write(b"$00I\n\r")
        time.sleep(0.3)
        received_frame = VT.read_all().decode('utf-8')
        word = received_frame.split(" ")
        strings = str(word[1])
        number = float(strings)
        strings2 = str(word[0])
        number2 = strings2[-6:]
        number3 = float(number2)
        return [number, number3]

    def order(self, value):
        try:
            VT.write(ON % value.get())
            # print("The new order is : {}".format(value.get()))
        except:
            print("too fast, please slow down")
