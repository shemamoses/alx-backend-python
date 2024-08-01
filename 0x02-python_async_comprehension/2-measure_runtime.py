#!/usr/bin/env python3
'''
Defines function that executes in parallel
'''
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''
    Measures runtime of async_comprehension
    '''
    begin = time.perf_counter()
    await asyncio.gather(*[async_comprehension() for i in range(4)])
    duration = time.perf_counter() - begin
    return duration
