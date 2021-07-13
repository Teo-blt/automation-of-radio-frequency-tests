#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 13 15:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import paramiko
from loguru import logger
import threading

# =============================================================================
THE_COLOR = "#E76145"


class Threadfilter(threading.Thread):

    def __init__(self, ip_address):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip_address = ip_address
        self.original_value = 0
        self.value = 0

    def run(self):
        self.read_original_value()
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_address, username=username, password=password)
        logger.debug(f"Successfully connected to {self.ip_address}")
        self.original_value = "867400000"
        cmd = "sed -i '3,8 s/" + self.original_value + "/" + str(self.value) + "/' /etc/lorad/zepto/EU868-FR.json"
        cmd2 = "cat /etc/lorad/zepto/EU868-FR.json"
        ssh.exec_command(cmd, get_pty=True)
        stdin, stdout, stderr = ssh.exec_command(cmd2, get_pty=True)

        while 1:
            wah = stdout.readline()
            print(wah)
            if wah[7:11] == "etid":
                ssh.close()
                break

    def read_original_value(self):
        username = "root"
        password = "root"
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip_address, username=username, password=password)
        cmd = "sed -n 6p /etc/lorad/zepto/EU868-FR.json"
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        wah = stdout.readline()
        self.original_value = wah[11:20]
        print(self.original_value)
