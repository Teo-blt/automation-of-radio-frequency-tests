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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.ip, username=username, password=password)
        logger.debug(f"Successfully connected to {self.ip}")
        cmd = "./lora_pkt_fwd -c global_conf.json.sx1250.EU868"
        cmd2 = "cd /user/libsx1302-utils_V1.0.5-klk1-dirty"
        stdin, stdout, stderr = ssh.exec_command(cmd2 + "\n" + cmd, get_pty=True)

        while (1):
            wah = stdout.readline()
            logger.info(wah)
            if wah[19:22] == "EUI":
                logger.debug("The iZepto is ready")
                break
        self.write_doc("Sensitivity measurement iZepto")
        wah1 = 0
        for i in range(0, 10):
            a = stdout.readline()
            print(a)
            wah1 = wah1 + len(a)
            logger.info(f"The number of frames receive is {wah1}")
            self.write_doc(f"The number of frames receive is {wah1}")
        logger.info("finish")
        self.write_doc("finish")
        ssh.close()

    def write_doc(self, text):
        izepto_result = open("Report_iZepto.txt", 'a')
        izepto_result.write(str(text) + "\n")
        izepto_result.close()
