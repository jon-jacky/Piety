"""
pmacsinit.py - define and initialize global variables used in pmacs module
"""

mark = 0 # line number, defines region for cut C_w etc.  0 means disabled.

promptline = edsel.flines+1 # line after end of edsel frame

prev_k = key.M_x # exit from pmacs

