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
import sys

# =============================================================================

CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
CONNECTION = 'COM11'

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
        self.temps = 0
        self.temperature = 0
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof
        self.root = my_auto_scale_frame
        self.FIRST_TIME = False
        self.VALUE_STABILISATION = 0
        self.i = 0
        self.temp = 0
        self.temp2 = 0
        self.cycle = 0
        self.time_start_min = 0

    def run(self):

        self.temps = 1/60

        if nlanla:
            self.temperature = self.temp_min
        else:
            self.temperature = self.temp_max

        VT.write(ON % self.temperature)

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

        global time_start
        time_start = time.time()

        print("\n################################################\n")
        print("\nStart of Test\n")

        if self.oof:
            self.off()

        self.loop(self.temperature, self.temps)
# ==============================================================================================

    def loop(self, order, timer):
        [self.temp, self.temp2] = self.read()
        print("#################################")
        print("The actual themperature is : {}".format(self.temp))
        print("The actual order is : {}".format(self.temp2))
        if self.temp != order:
            self.VALUE_STABILISATION = 0
            self.FIRST_TIME = False
            self.root.after(5000, lambda: self.loop(order, timer))  # => loop after 5 secondes
        elif abs(self.temp - order) < 0.2:
            if self.VALUE_STABILISATION < 60:
                print("The climate chamber is stabilized since {} seconds of the "
                      "60 request ".format(self.VALUE_STABILISATION))
                self.VALUE_STABILISATION = self.VALUE_STABILISATION + 5
                self.root.after(5000, lambda: self.loop(order, timer))
            else:
                if not self.FIRST_TIME:
                    print("The climate chamber is stabilized with success")
                    self.time_start_min = time.time()
                    self.FIRST_TIME = True
                a = time.localtime(self.time_start_min)
                b = time.localtime(time.time())
                c = time.localtime(self.time_start_min + (timer * 3600))
                print("The actual time is {} hours and {} minutes".format(b[3], b[4]))
                print("The test started at {} hours and {} minutes".format(a[3], a[4]))
                print("The test finish in {} hours and {} minutes".format(c[3], c[4]))
                if time.time() < self.time_start_min + (timer * 3600):
                    self.root.after(5000, lambda: self.loop(order, timer))  # => loop after 5 secondes
                else:
                    global time_start
                    print(f'End of cycle {self.i}: {time.time() - time_start}\n')
                    self.i = self.i + 1
                    self.cycle = self.cycle + 0.5
                    if self.cycle == self.nb_cycle:
                        self.exit()
                    else:
                        if order == self.temp_max:
                            VT.write(ON % self.temp_min)
                            self.FIRST_TIME = False
                            self.loop(self.temp_min, self.temp_min_duration_h)
                        else:
                            VT.write(ON % self.temp_max)
                            self.FIRST_TIME = False
                            self.loop(self.temp_max, self.temp_max_duration_h)


    def off(self):
        try:
            VT.write(CLIMATIC_CHAMBER_STOP)
        except:
            print("Error, the climate chamber is already offline")

    def exit(self):
        # Stop climatic chamber
        self.off()
        time_stop = time.time()
        print("\n################################################\n")
        print("\nEnd of Test\n")
        print(f'Test duration: {time_stop - time_start}\n')
        sys.exit()

    def read(self):
        try:
            VT.write(b"$00I\n\r")
            time.sleep(0.2)
            received_frame = VT.read_all().decode('utf-8')
            word = received_frame.split(" ")
            strings = str(word[1])
            number = float(strings)
            strings2 = str(word[0])
            number2 = strings2[-6:]
            number3 = float(number2)
            return [number, number3]
        except:
            print("too fast, please wait")
            return [0, 0]

    def order(self, value):
        try:
            VT.write(ON % value)
            # print("The new order is : {}".format(value.get()))
        except:
            print("too fast, please slow down")
