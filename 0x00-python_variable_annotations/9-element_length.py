#!/usr/bin/env python3
'''
Defines function to which determines length of list
'''
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''
    Returns list containing sub-lists and their lengths
    '''
    return [(i, len(i)) for i in lst]
