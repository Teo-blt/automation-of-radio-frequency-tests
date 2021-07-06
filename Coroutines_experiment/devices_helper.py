import serial
from loguru import logger
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
    logger.info("Scan in progress")
    for i in range(0, 30):
        test = ('COM' + str(i))
        try:
            serial.Serial(test, 9600, timeout=1, writeTimeout=1)
            data[a] = i
            a = a + 1
        except:
            pass
    values = list(data.values())
    logger.info(f"The available ports are : {values} ")
    return [a, values]


def scan_all_gpib(version):
    """
    Scan all gpib
    """
    if version:
        data = {}
        a = 0
        time = 1
        logger.info("New version scan in progress")
        [numbera, numberb] = scan_all_ports()
        for t in range(0, numbera):
            test1 = "COM" + str(numberb[t])
            ser = serial.Serial("COM18", 9600, timeout=time, write_timeout=time, inter_byte_timeout=time)
            for i in range(0, 30):
                test = str(i)
                ser.write(('++addr ' + test + '\n').encode())
                ser.write("*IDN?\r".encode())
                ans = ser.readlines(ser.write(('++read\n'.encode())))
                try:
                    word = ans[0]
                    word2 = word[10:11]
                    logger.info(f"The GPIB {i} is available")
                    data[a] = i
                    a = a + 1
                    break
                except:
                    pass
            values = list(data.values())
            logger.info(f"The available GPIB are : {values} ")
            return [a, values]

    else:
        data = {}
        a = 0
        time = 1
        logger.info("Old version scan in progress")
        for i in range(0, 30):
            test = str(abs((i - 30)))
            try:
                rm = visa.ResourceManager()
                smiq_send = rm.open_resource("GPIB0" + '::' + test + '::INSTR', timeout=time,
                                             write_timeout=time, inter_byte_timeout=time)
                smiq_send.write('*RST')
                logger.info(f"The GPIB {test} is available")
                data[a] = test
                a = a + 1  # TODO faster !
                break
            except:
                logger.debug(f"The GPIB {test} is unavailable")
        values = list(data.values())
        logger.info(f"The available GPIB are : {values} ")
        return [a, values]
