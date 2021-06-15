import pyvisa as visa
from tkinter import *
from loguru import logger
import sys


sys.path.append('P:\\e2b\\hardware\\Scripts_auto\\Python\\lib')
rm = visa.ResourceManager()
smiq_send = rm.open_resource('PROLOGIX::COM12::GPIB::20')
smiq_send.write('*RST')
logger.info(smiq_send.query('*IDN?'))
smiq_send.write('OUTP:STAT OFF')  # RF Output OFF
smiq_send.write('SOUR:DM:STAT ON')  # Digital Modulation ON
smiq_send.write('SOUR:DM:SOUR DLIST')  # Source selection
smiq_send.write("SOUR:DM:DLIST:SEL 'T1_TEST'")  # 169_N2
smiq_send.write('SOUR:DM:SEQ SINGLE')  # AUTO | RETRigger | AAUTo | ARETrigger | SINGle
# Rectangle filter mandatory for WM4800 !
smiq_send.write('SOUR:DM:FILT:TYPE RECT')
