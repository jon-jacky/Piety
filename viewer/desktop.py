# Start edsel editor with viewer panel: python3 -im desktop
# First must define PYTHONPATH by . /home/jon/Piety/bin/paths, once in session
import sked
from sked import *
import frame
from frame import *
import dmacs
from dmacs import dm # so we can revert to dmacs if edsel is broken
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
import viewer
from viewer import *
tl = edsel.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region 
vwin()
import desktop_startup # load buffers into editor

 
