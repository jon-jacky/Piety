"""
schedule.py - Data and functions used by both piety and eventloop modules.

This module is platform-independent, but it is imported by the
platform-dependent eventloop modules.
"""

import collections # for Counter, defaultdict

# Schedule data structure
# key, value: input, list of tasks waiting for data at that input
# Task __init__ puts each new task in this schedule, using its activate method
schedule = collections.defaultdict(list)

# Count events on each input. key: input, value: number of events on that input
ievent = collections.Counter()

timer = -1 # indicates timer input, not timeout interval
           # differs from any fd.fileno()

def handler(input):
    """
    Call the handlers for all the enabled tasks waiting for the input.
    Might call more than one handler for the same input.
    If only a single handler should be called for each input, 
    manage all the applications that handle the same input 
    as piety.Job instances in a single piety.Session task.
    """
    if input in schedule:
        for t in schedule[input]:
            if t.enabled():
                t.handler()
    ievent[input] += 1
              
              
