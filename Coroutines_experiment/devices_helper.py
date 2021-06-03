import serial
from loguru import logger
from Climate_chamber_control.Climate_chamber import SERIAL_SPEED
import pyvisa as visa


def open_port(new_port):
    """
    try to open this new port
    :param new_port:
    :return: opened port
    """
    try:
        new_port.open()
    except:
        pass

    return new_port


def scan_all_ports():
    """
    Scan all ports
    """
    data = {}
    a = 0
    logger.info("scan in progress")
    for i in range(0, 100):
        test = ('COM' + str(i))
        try:
            serial.Serial(test, SERIAL_SPEED, timeout=1, writeTimeout=1)
            logger.info(f"The connection port {i} is available")
            data[a] = i
            a = a + 1
        except:
            logger.debug(f"The connection port {i} is unavailable")
    values = list(data.values())
    logger.info(f"The available ports are : {values} ")
    return [a, values]


def scan_all_gpib(type_gpib):
    """
    Scan all gpib
    """
    data = {}
    a = 0
    logger.info("scan in progress")
    for i in range(0, 100):
        test = str(i)
        try:
            rm = visa.ResourceManager()
            smiq_send = rm.open_resource(type_gpib + '::' + test + '::INSTR')
            smiq_send.write('*RST')
            logger.info(f"The GPIB {i} is available")
            data[a] = i
            a = a + 1
        except:
            logger.debug(f"The GPIB {i} is unavailable")
    values = list(data.values())
    logger.info(f"The available GPIB are : {values} ")
    return [a, values]
