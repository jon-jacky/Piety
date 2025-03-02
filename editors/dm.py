# Start dmacs editor with browser from command line in any dir: python3 -im dm
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm
import urls
from urls import *
import get 
from get import *
import render 
from render import *
tl = dmacs.terminal.set_line_mode # type tl() to restore echo after crash
win(22)
dm()
