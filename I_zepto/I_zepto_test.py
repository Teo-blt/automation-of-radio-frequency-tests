#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 11 11:53:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import paramiko
import threading
from tkinter import *
import tkinter as tk
from loguru import logger
from tkinter import filedialog
from tkinter.messagebox import *

# =============================================================================
global is_killed
is_killed = 0
THE_COLOR = "#E76145"

def lunch_izepto(ip):
    Threadibts(ip).start()


class Threadibts(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip = ip

    def run(self):
        ip_address = self.ip
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip_address, username=username, password=password)
        print("Successfully connected to", ip_address)

        cmd = "/user/libsx1302-utils_V1.0.5-klk1-dirty/lora_pkt_fwd -c global_conf.json.sx1250.EU868"

        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

        for line in iter(stdout.readline, ""):
            print(line, end="")
        print('finished.')



