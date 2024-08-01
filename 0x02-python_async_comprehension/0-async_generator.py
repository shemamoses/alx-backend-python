#!/usr/bin/env python3
'''
Defines a coroutine called async_generator
'''
from typing import Generator
import random
import asyncio


async def async_generator() -> Generator[float, None, None]:
    '''
    Generator function loops to 10
    '''
    for i in range(10):
        yield random.uniform(0, 10)
        await asyncio.sleep(1)
