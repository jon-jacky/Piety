# Start edsel editor with pyshell from command line in any dir: python3 -im ted
# Like ed script but also imports writer, timers, pyshell for tasking expts. 
# When script exits you see edsel window and pysh >> (not >>>) REPL prompt.
# Type ted() to begin display editing, M-x to return to >>, exit()  when done
# First must define PYTHONPATH by . ~/Piety/bin/paths, once in terminal session
import sked
from sked import *
import frame
from frame import *
import krebs
from krebs import kb # so we can revert to krebs if edsel is broken
import editline
import edsel
from edsel import ed, red # use red when starting from pysh instead of >>>
import pyshell
from pyshell import pysh, ted # from pysh, use ted not red to clear cmd_mode
import writer # for tasks
from writer import *
import timers # for tasks         
from timers import *
from contextlib import redirect_stdout # for tasks
import threading
from threading import Thread
threads = threading.enumerate # NOT from threading import enumerate. Name clash!
tl = edsel.terminal.set_line_mode # type tl() to restore echo after crash
from terminal_util import dimensions
tlines, tcols = dimensions()
win(tlines-8) # 8  lines in prompt + repl region  
from pyshell import ted # overwrite ted module in REPL with ted function
pysh() # Now at pysh >> prompt type ted() for display editing, exit() when done
 
