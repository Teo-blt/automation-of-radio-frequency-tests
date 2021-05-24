#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 10 11:22:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import asyncio
import sys
from loguru import logger
import threading
import time
from tkinter import *
import serial

# =============================================================================

global relaunch_safety
# noinspection PyRedeclaration
relaunch_safety = 0

CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
CONNECTION = '[None]'
vt = serial.Serial()


class Thread(threading.Thread):

    def __init__(self, port, temp_min, temp_max, temp_min_duration_h, temp_max_duration_h,
                 nb_cycle, oof, my_auto_scale_frame, up_down, stair, stair_temp, temperature_end):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)

        # additional data added to the class
        self.temp_min = temp_min
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
        self.timer = 0
        self.stair = stair
        self.stair_temp = stair_temp
        self.temperature_end = temperature_end
        self._port = port
        self.extinct = 0

    def run(self):
        global relaunch_safety
        if relaunch_safety == 0:  # To forbid the user to multi launch the program
            relaunch_safety = 1
            if self.oof:
                self.off()  # To shut down the climate chamber
            if self.up_down:  # The user can chose if he want to start with the lowest or the hottest temperature
                self.temperature = self.temp_min
                self.timer = self.temp_min_duration_h
            else:
                self.temperature = self.temp_max
                self.timer = self.temp_max_duration_h
            vt.write(ON % self.temperature)  # Send the order to the climate chamber
            [self.temp, self.temp2] = self.read(self._port)  # Use the function reed to get temp et temp2,
            # respectively actual temperature and order, the function reed ask directly to
            # the climate chamber the values, it's take time, but the value are much safer
            logger.info("################################################")
            logger.info("Start of Test")
            self.time_start = time.time()  # Collect the time of the beginning of the test
            #self.timer = 1 / 60  # For the test, it reduce the time of waiting to 1 min
            asyncio.run(self.several_methods_run_together())

    async def wait_temperature_reach_consign(self, timer):
        while abs(self.temp - self.temperature) >= 0.2 or self.VALUE_STABILISATION <= 120:
            # The maximal difference between the actual temperature and the order must be less than 0.2
            # (if we use a maximal difference of 0 it's take too much time to stabilize) AND the VALUE_STABILISATION
            # must be bigger than 120
            await asyncio.sleep(5)  # Like a wait but it will NOT freeze the program
            [self.temp, self.temp2] = self.read(self._port)  # Reed the value thanks to the reed function
            logger.info("#################################")  # show the values to the user
            logger.info(f"The actual temperature is : {self.temp}")
            logger.info("The actual order is : {}".format(self.temp2))
            if abs(self.temp - self.temperature) < 0.2:  # If the maximal difference between the actual temperature
                # and the order is less than 0.2, launch the countdown.
                logger.info("The climate chamber is stabilized since {} seconds of the "
                            "120 request ".format(self.VALUE_STABILISATION))
                self.VALUE_STABILISATION = self.VALUE_STABILISATION + 5  # Because the loop cycle every 5 seconds, we
                # add 5 to the VALUE_STABILISATION
            else:  # If the maximal difference between the actual temperature and the order is 0.2 or more we
                # reset the VALUE_STABILISATION
                self.VALUE_STABILISATION = 0
        logger.info("The climate chamber is stabilized with success")  # Said to the user When the
        # climate chamber is stabilized
        self.time_start_min = time.time()  # Collect the actual time named time_start_min for the waiting loop
        while time.time() < self.time_start_min + (timer * 3600):  # While the actual
            # time is smaller than the time_start_min WITH added with the timer, the while is looping
            await asyncio.sleep(5)  # Like a wait but it will NOT freeze the program
            [self.temp, self.temp2] = self.read(self._port)  # Reed the value thanks to the reed function
            logger.info("#################################")  # show the values to the user
            logger.info(f"The actual temperature is : {self.temp}")
            logger.info("The actual order is : {}".format(self.temp2))
            b = time.localtime(abs((self.time_start_min + (timer * 3600)) - time.time()))  # Show useful values
            # of time for the user
            c = time.localtime(self.time_start_min + (timer * 3600))
            logger.info("This half cycle will finish at {}H {}min and {} second(s)".format(c[3], c[4], c[5]))
            logger.info("{} hour(s) {} minute(s) and {} seconds remain".format(b[3] - 1, b[4], b[5]))
        return 1  # without a return, the while loop will run continuously.

    async def do_something_else(self):
        pass  # The function is no more use, but in case of...

    async def several_methods_run_together(self):
        if self.stair == 0:  # A variable to direct the program in function of the chose of the user,
            # here it's the loop for cycle
            while self.nb_cycle != self.cycle:  # While the number of cycle is not reach
                statements = [self.wait_temperature_reach_consign(self.timer), self.do_something_else()]  # The two
                # functions that need to run at the same time
                await asyncio.gather(*statements)  # Gather is used to allow both functions to run at the same time.*
                self.cycle = self.cycle + 0.5  # In mode cycle, reach the temperature and stabilize is half of a cycle
                if self.temperature == self.temp_max:  # switch between high order and low order, if the order was
                    # temp_max, it become temp min and if the order was temp in it become temp_max
                    vt.write(ON % self.temp_min)
                    self.temperature = self.temp_min
                else:
                    vt.write(ON % self.temp_max)
                    self.temperature = self.temp_max
                self.i = self.i + 1  # A variable to cunt the number of cycle (we could use self.cycle, but anyway
                a = time.localtime(time.time())  # collect the actual time
                # (not very useful because logger.info write time too)
                logger.info(f'End of cycle {self.i}: {a[3]}H{a[4]} and {a[5]} second(s)')  # some useful
                # information for the user
            self.exit()  # leave the program thanks to the function exit
        else:  # A variable to direct the program in function of the chose of the user, here it's the loop for stair
            if self.temperature >= self.stair_temp:  # simple condition to know if the order need to climb or go down
                self.stair_temp = -self.stair_temp
            while abs(self.temperature - self.temperature_end) >= abs(self.stair_temp):  # The maximal
                # difference between the actual order and the goal temperature must be less than the absolute value
                # of stair_temp, witch is the step between two level of temperature
                statements = [self.wait_temperature_reach_consign(self.timer), self.do_something_else()]  # The two
                # functions that need to run at the same time
                await asyncio.gather(*statements)  # Gather is used to allow both functions to run at the same time.*
                self.temperature = self.temperature + self.stair_temp  # we add or remove stair_temp to the order
                # of the climatic chamber
                if self.temperature > 80 or self.temperature < -40:  # To prevent extreme temperature, the program
                    # will leave automatically
                    self.exit()  # We use the function exit to leave the program
                vt.write(ON % self.temperature)  # Sending of the new order to the climatic chamber
                self.i = self.i + 1  # A variable to cunt the number of cycle
                a = time.localtime(time.time())
                logger.info(f'End of cycle {self.i}: {a[3]}H{a[4]} and {a[5]} second(s)')  # some useful
                # information for the user

            self.exit()  # leave the program thanks to the function exit

    def exit(self):
        self.off()  # Use the off function to stop the climatic chamber # TODO repair the sys.exit() #a réparer
        time_stop = time.time()
        logger.info("################################################")
        logger.info("End of Test")
        b = time.localtime(time_stop - self.time_start)  # Total time of the test
        logger.info(f'Test duration: {b[3]}H{b[4]} and {b[5]} second(s)')  # some useful information for the user
        sys.exit()  # TODO repair the sys.exit() #a réparer

    def read(self, the_port):
        try:  # This try allow the program to survive in a rare case where the climatic
            # chamber don't have enough time to answer back
            self._port = the_port
            vt.port = self._port
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
            logger.error("too fast, please wait")  # protect the application if the user
            # make a request the same time than the programme
            return [0, "None"]  # In case of an error, this function will return [0,0], This will NOT affect the graph

    def order(self, value):  # A very simple function use in the manual mode
        try:  # This try allow to save the program when, in rare case, spamming the Send button
            # of the manual mode produce an error
            vt.port = self._port
            vt.timeout = 5
            vt.writeTimeout = 1
            try:
                vt.open()
            except:
                pass
            vt.write(ON % value)
        except serial.serialutil.SerialTimeoutException:
            logger.error(f"The port[{self._port}] is not link to the climate chamber")
        except:
            logger.error("too fast, please slow down")

    def off(self):  # The function off, shut down the climatic chamber and reset the relaunch_safety variable
        # that was use to control the multi launching of the program
        vt.port = self._port
        try:
            vt.open()
        except:
            pass
        vt.write(CLIMATIC_CHAMBER_STOP)  # Stop the climatic chamber
        global relaunch_safety  # relaunch_safety variable
        relaunch_safety = 0
        logger.debug("The climate chamber was correctly arrest")
