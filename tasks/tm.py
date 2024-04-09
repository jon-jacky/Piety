# Start pmacs editor with pyshell from command line in any dir: python3 -im tm
# Like pm script but also imports writer, timers, pyshell for tasking expts. 
# When script exits you see pmacs window and pysh >> (not >>>) REPL prompt.
# Type rpm() to begin display editing, M-x to return to >>, exit()  when done
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm # so we can revert to dmacs if pmacs is broken
import editline
import pmacs
from pmacs import pm, rpm # use rpm when starting from pysh instead of >>>
import pyshell
from pyshell import pysh, tpm # from pysh, use tpm not rpm to clear cmd_mode
import writer # for tasks
from writer import *
import timers # for tasks         
from timers import *
from contextlib import redirect_stdout # for tasks
from threading import Thread
from threading import enumerate
tl = pmacs.terminal.set_line_mode # type tl() to restore echo after crash
win(22)
pysh() # Now at pysh >> prompt type rpm() for display editing, exit()  when done


