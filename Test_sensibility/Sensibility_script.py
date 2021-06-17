#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 17 11:30:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import asyncio
import time

# =============================================================================

async def func_a():
    print("a")

async def func_b():
    time.sleep(5)
    print("b")

async def several_methods_run_together():
    statements = [func_a(), func_b()]
    await asyncio.gather(*statements)
    print("c")

asyncio.run(several_methods_run_together())