#!/usr/bin/env python3
'''
Asynchronous coroutine waits for a random delay between 0 and max_delay
'''
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    '''
    Function waits for duration and returns the random integer after completed
    '''
    random_duration = random.uniform(0, max_delay)
    await asyncio.sleep(random_duration)
    return random_duration
