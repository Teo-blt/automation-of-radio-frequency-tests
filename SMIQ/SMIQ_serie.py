#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 25 16:04:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests in python language"""
# =============================================================================
import pyvisa as visa
import serial
import os
import time
import sys
import threading
from tkinter import *
import tkinter as tk
# =============================================================================
SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
CONNECTION = 'COM5'
a = serial.Serial(CONNECTION, SERIAL_SPEED, timeout=SERIAL_TIMEOUT, writeTimeout=SERIAL_TIMEOUT)