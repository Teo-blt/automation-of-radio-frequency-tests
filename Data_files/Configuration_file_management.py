#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: July 7 10:53:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
from loguru import logger
# =============================================================================


file_name = "Orders.txt"
file = open(file_name, "r")
donnees = []
p = 0
for line in file:
    donnees = donnees + line.rstrip('\n\r').split("=")
    p += 1
logger.info(f"The file name is: {file_name}")
for n in range(0, 2 * p, 2):
    logger.info(f"The command of the {donnees[n]} is: {donnees[n + 1]}")

file.close()