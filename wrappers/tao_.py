"""
tao_.py, wrapper for tao.py from https://github.com/nyxyn/tao

"""

import sys

# Avoid name clashes.  In a Piety session, import this module by:
# import tao_ as tao
# Here we import the installed program, 
# must simulate command line args because code that runs on import uses them
sys.argv = ['tao'] # no argv[1]
import tao as _tao

# In a Piety session, invoke this program with tao.main() to print random
# chapter or tao.main(42) to print chapter 42.

def main(*chapter):
    # simulate command line args so run can find them
    sys.argv = ['tao']
    if chapter:
        sys.argv.append(str(chapter[0]))

    # FIXME - very inefficient, loads json for entire book each time
    _tao.run()


