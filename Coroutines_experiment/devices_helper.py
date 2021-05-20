import serial
from loguru import logger
from Climate_chamber_control.Climate_chamber import SERIAL_SPEED, SERIAL_TIMEOUT


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


def scan_all_ports(already_connected_port: str):
    """
    Scan all ports
    :param already_connected_port: already connected port
    """
    data = {}
    a = 0
    for i in range(0, 100):
        test = ('COM' + str(i))
        try:
            serial.Serial(test, SERIAL_SPEED, timeout=1, writeTimeout=1)
            logger.info(f"The connection port {i} is available")
            data[a] = i
            a = a + 1
        except:
            if test == already_connected_port:
                logger.critical(f"You are actually trying to connect to the port {i} ")
            else:
                logger.debug(f"The connection port {i} is unavailable")
    values = list(data.values())
    logger.info(f"The available ports are : {values} ")
    return [a, values]
