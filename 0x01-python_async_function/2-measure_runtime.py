#!/usr/bin/env python3
'''
Defines function to measure time taken for the function to run
'''
import time
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    '''
    Returns time taken to complete performance
    '''
    begin = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = time.perf_counter() - begin
    return(end)
