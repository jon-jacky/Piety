# Start edsel editor without desktop from command line: python3 -im ed
# First must define PYTHONPATH by . /home/jon/Piety/bin/paths, once in session
import sked
from sked import *
import frame
from frame import *
import krebs
from krebs import kb # so we can revert to krebs if edsel is broken
import console
from console import *
import editline
import disable_eventloop # prevents edsel from importing eventloop
import edsel
import urls
from urls import *
import get
from get import *
import render 
from render import *
import search
from search import *
tl = edsel.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region  
from edsel import ed # overwrite ed imported from frame get render etc. ...
# Put some text in the Python REPL
print("""
>>> # This is the Python interpreter.
>>> # Type alt-X to enter the interpreter.
>>> # Type ed() to return to visual editing in windows.
>>> """)
ed() # start display editing in editor window
