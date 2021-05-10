import asyncio
from loguru import logger
import threading
import time
import serial

SERIAL_SPEED = 9600
SERIAL_TIMEOUT = 5
CONNECTION = 'COM11'

try:
    VT = serial.Serial(CONNECTION, SERIAL_SPEED, timeout=SERIAL_TIMEOUT)
except:
    logger.critical("Connection not possible")
    logger.critical("Please chek your connection port")


class Mythread(threading.Thread):

    def __init__(self, temp_min, temp_max, temp_min_duration_h,
                 temp_max_duration_h, nb_cycle, oof, my_auto_scale_frame, up_down):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.temp_min = temp_min  # additional data added to the class
        self.temp_max = temp_max
        self.temps = 0
        self.temperature = 0
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof
        self.root = my_auto_scale_frame
        self.FIRST_TIME = False
        self.VALUE_STABILISATION = 0
        self.i = 0
        self.temp = 0
        self.temp2 = 0
        self.cycle = 0
        self.time_start_min = 0
        self.up_down = up_down

    def run(self):
        asyncio.run(self.several_methods_run_together())

    async def wait_temperature_reach_consign(self, consign: int):
        logger.info("start wait_temperature_reach_consign()")
        inTemp: int = 0
        while inTemp != consign:
            await asyncio.sleep(1)
            [self.temp, self.temp2] = self.read()
            logger.info("#################################")
            logger.info(f"The actual themperature is : {self.temp}")
            logger.info("The actual order is : {}".format(self.temp2))

        logger.info("finish wait_temperature_reach_consign()")
        return inTemp  # without a return, the while loop will run continuously.

    async def do_something_else(self):
        for i in range(0, 100):
            await asyncio.sleep(2)
            logger.info(f"do_something_else {i}")

    async def several_methods_run_together(self):
        statements = [self.wait_temperature_reach_consign(10), self.do_something_else()]
        logger.info("start several_methods_run_together()")
        await asyncio.gather(*statements)  # Gather is used to allow both funtions to run at the same time.
        logger.info("finish several_methods_run_together()")

    def read(self):
        try:
            VT.write(b"$00I\n\r")
            time.sleep(0.2)
            received_frame = VT.read_all().decode('utf-8')
            word = received_frame.split(" ")
            strings = str(word[1])
            number = float(strings)
            strings2 = str(word[0])
            number2 = strings2[-6:]
            number3 = float(number2)
            return [number, number3]
        except:
            logger.error("too fast, please wait")
            return [0, 0]

Mythread(-1, 1, 1, 1, 1, 0, 0, 1).start()