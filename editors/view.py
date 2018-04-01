"""
view.py - configuration variables assigned/used by both ed and edsel
"""

import sys, os

def noupdate(op, **kwargs): 
    pass 

null = open(os.devnull, 'w') # discard l z printed output in display editor

# Configuration for ed line editor
update = noupdate # ed has no display, update does nothing
lz_print_dest = sys.stdout  # ed l and z commands print in scroll region
