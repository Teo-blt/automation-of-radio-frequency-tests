#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 22 15:20:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
from loguru import logger
from tkinter import *
import serial

# =============================================================================


CLIMATIC_CHAMBER_STOP = b"$00E 0000.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
ON = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
WRITE_TIMEOUT = 5
CONNECTION = '[None]'

