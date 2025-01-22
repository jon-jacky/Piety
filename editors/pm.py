# Start pmacs editor from command line in any dir: python3 -im pm
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm # so we can revert to dmacs if pmacs is broken
import host
import redirect
from redirect import *
import get
from get import *
import editline
import pmacs
from pmacs import pm
tl = pmacs.terminal.set_line_mode # type tl() to restore echo after crash
win(26)
pm()
