"""
tao_.py, print a chapter from the Tao Te Ching.

Wrapper for tao.py from https://github.com/nyxyn/tao

To import this wrapper:

  import tao_ as tao

To print a random chapter:

  tao.main()

To print chapter 42 (etc.):

  tao.main(42)

This wrapper invokes the original tao.py script from github without any
changes, so it prints a chapter on initial import, then rereads the same
json file with the entire book text every time it is invoked.

This wrapper is named tao_.py (with a trailing underscore) to avoid a
name clash with the original tao.py.  We must import both.
"""

import sys

# import the installed program,
# must simulate command line args because code that runs on import uses them
sys.argv = ['tao'] # no argv[1]
import tao as _tao

def main(*chapter):
    # simulate command line args so run can find them
    sys.argv = ['tao']
    if chapter:
        sys.argv.append(str(chapter[0]))

    _tao.run()

