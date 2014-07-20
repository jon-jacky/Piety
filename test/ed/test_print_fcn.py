"""
Test redirecting printing with file=... arg
"""
# https://docs.python.org/2.7/library/functions.html#print
# says this works since 2.6
from __future__ import print_function

import sys

class Buffer(object):
    def __init__(self):
        self.lines = [] # list of strings

    def write(self, s):
        self.lines.append(s)

buffer = Buffer()

# Try reassign buffer.lines to destination
destination = sys.stdout

def printf(s):
    print(s, file=destination)
