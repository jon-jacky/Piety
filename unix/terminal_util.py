"""
terminal_util.py - functions that work when stdin is not a terminal
                    use even when piping input from a script
"""

import subprocess # just for display dimensions

def dimensions():
    'Return nlines, ncols. Works on Mac OS X, probably other Unix.'
    nlines = int(subprocess.check_output(['tput','lines']))
    ncols = int(subprocess.check_output(['tput','cols']))
    return nlines, ncols
