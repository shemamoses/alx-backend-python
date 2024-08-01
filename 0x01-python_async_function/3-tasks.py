#!/usr/bin/env python3
'''
Defines function that returns asyncio.Task from a coroutine
'''
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    '''
    returns wait_random task
    '''
    return asyncio.create_task(wait_random(max_delay))
