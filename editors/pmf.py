# Start pmacs editor full screen with viewer panel in any dir: python3 -im pmf
# First must define PYTHONPATH by . /home/jon/piety/bin/paths, once in session
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
tl = pmacs.terminal.set_line_mode # type tl() to restore echo after crash
win(24) 
vwin()
pm()
