#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 10 11:22:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import asyncio
from loguru import logger
import threading
import time
import serial
from tkinter import *

# =============================================================================
CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
CONNECTION = 'COM11'

try:
    VT = serial.Serial(CONNECTION, SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
except:
    logger.critical("Connection not possible")
    logger.critical("Please chek your connection port")


class Mythread(threading.Thread):

    def __init__(self, temp_min, temp_max, temp_min_duration_h,temp_max_duration_h,
                 nb_cycle, oof, my_auto_scale_frame, up_down, stair, stair_temp):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.temp_min = temp_min  # additional data added to the class
        self.temp_max = temp_max
        self.time_start = 0
        self.temps = 0
        self.temperature = 0
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof
        self.root = my_auto_scale_frame
        self.VALUE_STABILISATION = 0
        self.i = 0
        self.temp = 0
        self.temp2 = 0
        self.cycle = 0
        self.time_start_min = 0
        self.up_down = up_down
        self.timer = 1 / 60
        self.stair = stair
        self.stair_temp = stair_temp

    def run(self):
        if self.oof:
            self.off()
        if self.up_down:
            self.temperature = self.temp_min
            self.timer = self.temp_min_duration_h
        else:
            self.temperature = self.temp_max
            self.timer = self.temp_max_duration_h
        VT.write(ON % self.temperature)
        p = 0
        while p < 1:
            logger.debug("start-up, please wait")
            time.sleep(2)
            logger.debug("start-up, please wait.")
            time.sleep(2)
            logger.debug("start-up, please wait..")
            time.sleep(2)
            logger.debug("start-up, please wait...")
            time.sleep(2)
            p = p + 1
        [self.temp, self.temp2] = self.read()
        logger.info("################################################")
        logger.info("Start of Test")
        self.time_start = time.time()
        self.timer = 1 / 60
        asyncio.run(self.several_methods_run_together())

    async def wait_temperature_reach_consign(self, timer):
        while abs(self.temp - self.temperature) >= 0.2 or self.VALUE_STABILISATION <= 120:
            await asyncio.sleep(5)
            [self.temp, self.temp2] = self.read()
            logger.info("#################################")
            logger.info(f"The actual temperature is : {self.temp}")
            logger.info("The actual order is : {}".format(self.temp2))
            if abs(self.temp - self.temperature) < 0.2:
                logger.info("The climate chamber is stabilized since {} seconds of the "
                            "120 request ".format(self.VALUE_STABILISATION))
                self.VALUE_STABILISATION = self.VALUE_STABILISATION + 5
            else:
                self.VALUE_STABILISATION = 0
        logger.info("The climate chamber is stabilized with success")
        self.time_start_min = time.time()
        while time.time() < self.time_start_min + (timer * 3600):
            await asyncio.sleep(5)
            [self.temp, self.temp2] = self.read()
            logger.info("#################################")
            logger.info(f"The actual temperature is : {self.temp}")
            logger.info("The actual order is : {}".format(self.temp2))
            b = time.localtime(abs((self.time_start_min + (timer * 3600)) - time.time()))
            c = time.localtime(self.time_start_min + (timer * 3600))
            logger.info("The test will finish at {}H {}min and {} second(s)".format(c[3], c[4], c[5]))
            logger.info("{} hour(s) {} minute(s) and {} seconds remain".format(b[3]-1, b[4], b[5]))
        return 1  # without a return, the while loop will run continuously.

    async def do_something_else(self):
        pass

    async def several_methods_run_together(self):
        while self.nb_cycle != self.cycle:
            statements = [self.wait_temperature_reach_consign(self.timer), self.do_something_else()]
            await asyncio.gather(*statements)  # Gather is used to allow both functions to run at the same time.*
            self.cycle = self.cycle + 0.5

            if self.stair == 0:
                if self.temperature == self.temp_max:
                    VT.write(ON % self.temp_min)
                    self.temperature = self.temp_min
                else:
                    VT.write(ON % self.temp_max)
                    self.temperature = self.temp_max
            else:
                self.temperature = self.temperature + self.stair_temp
                if self.temperature > 80 or self.temperature < -40:
                    self.exit()

            self.i = self.i + 1
            a = time.localtime(time.time())
            logger.info(f'End of cycle {self.i}: {a[3]}H{a[4]} and {a[5]} second(s)')
        self.exit()

    def off(self):
        try:
            VT.write(CLIMATIC_CHAMBER_STOP)
        except:
            logger.error("Error, the climate chamber is already offline")

    def exit(self):
        # Stop climatic chamber
        self.off()
        time_stop = time.time()
        logger.info("################################################")
        logger.info("End of Test")
        b = time.localtime(time_stop - self.time_start)
        logger.info(f'Test duration: {b}')
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
            logger.error("too fast, please wait")
            return [0, 0]

    def order(self, value):
        try:
            VT.write(ON % value)
            # print("The new order is : {}".format(value.get()))
        except:
            logger.error("too fast, please slow down")
