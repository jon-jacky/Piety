# apm.py - script to start asynchronous pmacs in a piety session
#
#  ...$ python -m piety
#  >>>> run(apm.py)
#  ... window appears ...

import sked
from sked import *
import edsel  
from edsel import *
from apmacs import apm

win(22)
apm()


