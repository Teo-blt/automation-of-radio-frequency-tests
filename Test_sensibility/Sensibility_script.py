#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 17 11:30:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import asyncio
import threading
from tkinter import *
import time
from I_zepto import I_zepto_test
from SSH import Test_SSH
# =============================================================================
THE_COLOR = "#E76145"
global validation
validation = 0

class Sensibility(threading.Thread):

    def __init__(self, ip_address, ip):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip = ip
        self.ip_address = ip_address

    def run(self):
        asyncio.run(self.several_methods_run_together())

    async def func_a(self):
        global validation
        I_zepto_test.lunch_izepto(self.ip)
        validation = validation + 1

    async def func_b(self):
        global validation
        Test_SSH.lunch_ibts(self.ip_address)
        validation = validation + 1

    async def func_c(self):
        global validation
        for i in range(0, 10):
            print("c" + str(i))
            time.sleep(1)
        validation = validation + 1

    async def several_methods_run_together(self):
        statements = [self.func_a(), self.func_b(), self.func_c()]
        truc = Tk()
        truc.title("truc test")
        await asyncio.gather(*statements)
        if validation == 3:
            print("d")


