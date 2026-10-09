# Start krebs editor with browser from command line in any dir: python3 -im kb
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import frame
from frame import *
import krebs
import console
from console import *
import urls
from urls import *
import get 
from get import *
import render 
from render import *
import search
from search import *
tl = krebs.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region  
# Put some text in the Python REPL
print("""
>>> #
>>> #
>>> # You rang?
>>> """)
from krebs import kb  # overwrite krebs as kb module defn with kb fcn defn
kb() # start display editing in editor window
