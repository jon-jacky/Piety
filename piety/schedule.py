"""
schedule.py - Data and functions used by both peity and eventloop.
              Move them out of piety module to break circular dependency.

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
    Call the handlers for all the enabled tasks waiting for this input.
    """
    if input in schedule:
        for t in schedule[input]:
            if t.enabled():
                t.handler()
                # break # FIXME? we consumed data from input, might be no more
                # This break might be needed for inputs that provide data
                # that is consumed, but not for timer input
    else:
        pass
    ievent[input] += 1
              
              
