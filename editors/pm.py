# Start pmacs editor from command line in any dir: python3 -im pm
# First must define PYTHONPATH by . /Users/jon/piety/bin/paths, once in session
import sked
from sked import *
import edsel
from edsel import *
import dmacs
from dmacs import dm # so we can revert to dmacs if pmacs is broken
import pmacs
from pmacs import pm
win(24)
pm()
