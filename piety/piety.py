# piety.py - like viewer/desktop.py but also imports piety async tasking
# First must define PYTHONPATH by . /home/jon/Piety/bin/paths, once in session
# Imports eventloop, defines piety (the eventloop) and startpiety 
# (the function) at top level.
# Does not start the eventloop, user must call startpiety()

import sked
from sked import *
import frame
from frame import *
import krebs
from krebs import kb # so we can revert to krebs if edsel is broken
import console
from console import *
import editline
import edsel
import urls
from urls import *
import get
from get import *
import render 
from render import *
import search
from search import *
import viewer
from viewer import *
# import the async machinery but don't start it yet
import eventloop
# don't call startpiety yet
from eventloop import piety, startpiety, stoppiety, tasks, block 
import aiotimers
from aiotimers import timer, starttimer, stoptimer, onetimer, twotimers
import aclock
from aclock import startclock, stopclock, ca, ta
# display the windows
tl = edsel.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region 
vwin() 
import piety_startup # load several buffers desktop.txt keys.txt etc.
# Make it so we can always type ed() whether or not eventloop is running.
from aedsel import ed # This ed function name overrides sked as ed module name
ed()

