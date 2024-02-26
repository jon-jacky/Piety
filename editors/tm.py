# Start pmacs editor from command line in any dir: python3 -im tm
# Like pm script but also imports writer and timers modules for tasking expts.
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm # so we can revert to dmacs if pmacs is broken
import editline
import pmacs
from pmacs import pm
import writer # for tasks
from writer import *
import timers # for tasks         
from timers import *
from contextlib import redirect_stdout # for tasks
from threading import Thread
from threading import enumerate
tl = pmacs.terminal.set_line_mode # type tl() to restore echo after crash
win(22)
pm()
