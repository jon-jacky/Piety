# piety.py - like viewer/desktop.py but starts piety async shell etc to >>>>
# First must define PYTHONPATH by . /home/jon/piety/bin/paths, once in session
# imports eventloop, 
# Defines piety (the eventloop) and piety_start (the function) at top level
# At the end, starts the eventloop and async shell
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm # so we can revert to dmacs if pmacs is broken
import console
from console import *
import editline
import pmacs
from pmacs import pm
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
from eventloop import piety, piety_start # But don't call piety_start() yet
from apmacs import apm # eventloop imports apmacs too but put apm at top level
# display the windows
tl = pmacs.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region 
vwin() 
import piety_startup  # load several buffers desktop.txt keys.txt etc.
piety_start() # start the eventloop and the async shell

 
