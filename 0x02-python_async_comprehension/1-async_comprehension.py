#!/usr/bin/env python3
'''
Defines a coroutine that collects 10m random numbs with async comprehensing
'''
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    '''
    Gathers all data from a genarator and returns them
    '''
    return [i async for i in async_generator()]
