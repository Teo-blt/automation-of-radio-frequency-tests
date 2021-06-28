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
# =============================================================================

def lunch_izepto(ip):
    Threadizepto(ip).start()


class Threadizepto(threading.Thread):

    def __init__(self, ip):
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        # additional data added to the class
        self.ip = ip

    def run(self):
        izepto_result = open("Report_iZepto.txt", 'w+')
        izepto_result.close()
        username = "root"
        password = "root"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, username=username, password=password)
        logger.debug(f"Successfully connected to {self.ip}")
        cmd = "./lora_pkt_fwd -c global_conf.json.sx1250.EU868"
        cmd2 = "cd /user/libsx1302-utils_V1.0.5-klk1-dirty"
        stdin, stdout, stderr = self.ssh.exec_command(cmd2 + "\n" + cmd, get_pty=True)

        while (1):
            wah = stdout.readline()
            if wah[0:5] == "ERROR":
                logger.critical("Failed to start the concentrator")
                logger.critical("Please restart the Izepto")

            if wah[19:22] == "EUI":
                logger.debug("The iZepto is ready")
                break

        self.write_doc("Sensitivity measurement iZepto")
        a = stdout.readline()
        time.sleep(20)
        self.ssh.close()
        a = stdout.readlines()
        number = ((len(a) + 1)/4)
        print(number)

    def write_doc(self, text):
        izepto_result = open("Report_iZepto.txt", 'a')
        izepto_result.write(str(text) + "\n")
        izepto_result.close()
