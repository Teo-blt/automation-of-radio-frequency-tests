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
from loguru import logger
import time
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

# =============================================================================

def lunch_izepto(ip, order_file):
    Threadizepto(ip, order_file).start()


class Threadizepto(threading.Thread):

    def __init__(self, ip, order_file):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip = ip
        self.file_name = order_file

    def run(self):
        izepto_result = open("Report_iZepto.txt", 'w+')
        izepto_result.close()
        username = "root"
        password = "root"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, username=username, password=password)
        logger.debug(f"Successfully connected to {self.ip}")

        cmd = self.file_execution(self.file_name, 3) + "\n" + self.file_execution(self.file_name, 5)
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True)

        while 1:
            wah = stdout.readline()
            if wah[0:5] == "ERROR":
                logger.critical("Failed to start the concentrator")
                logger.critical("Please restart the Izepto")
                self.ssh.exec_command("reboot", get_pty=True)
                logger.info("Izepto rebooting, it may take few minutes")

            if wah[19:22] == "EUI":
                logger.debug("The iZepto is ready")
                break

        self.write_doc("Sensitivity measurement iZepto")
        a = stdout.readline()
        time.sleep(20)
        self.ssh.close()
        a = stdout.readlines()
        number = ((len(a) + 1) / 4)
        print(number)

    def write_doc(self, text):
        izepto_result = open("Report_iZepto.txt", 'a')
        izepto_result.write(str(text) + "\n")
        izepto_result.close()

    def file_execution(self,file_name, n):
        a = []
        i = 0
        file_path = ''
        while sys.path[1].split('\\')[i] != 'automation-of-radio-frequency-tests':
            a.append(sys.path[1].split('\\')[i])
            i += 1
        for p in range(0, len(a)):
            file_path += str(a[p]) + '\\\\'
        file_path += 'automation-of-radio-frequency-tests\\\\Order_files\\\\'
        file_name = file_path + "Orders.txt"
        file = open(file_name, "r")
        donnees = []
        p = 0
        for line in file:
            donnees = donnees + line.rstrip('\n\r').split("=")
            p += 1
        file.close()
        return donnees[n]
