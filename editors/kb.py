# Start krebs editor with browser from command line in any dir: python3 -im kb
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import frame
from frame import *
import krebs
from krebs import kb
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
win(22)
kb()
