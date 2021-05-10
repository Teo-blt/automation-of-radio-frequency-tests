import asyncio
import random
from loguru import logger


async def wait_temperature_reach_consign(consign: int):
    logger.info("start wait_temperature_reach_consign()")
    inTemp: int = 0
    while inTemp <= consign:
        await asyncio.sleep(1)

        inTemp += random.random()
        logger.info(f"temperature = {inTemp}")

    logger.info("finish wait_temperature_reach_consign()")
    return inTemp  # without a return, the while loop will run continuously.


async def do_something_else(bound: int):
    logger.info("start do_something_else()")
    for i in range(0, bound):
        await asyncio.sleep(2)
        logger.info(f"do_something_else {i}")

    logger.info("finish do_something_else()")


async def several_methods_run_together():
    statements = [wait_temperature_reach_consign(10), do_something_else(12)]
    logger.info("start several_methods_run_together()")
    await asyncio.gather(*statements)  # Gather is used to allow both funtions to run at the same time.
    logger.info("finish several_methods_run_together()")


if __name__ == '__main__':
    logger.info("start main()")
    asyncio.run(several_methods_run_together())
    logger.info("finish main()")
