"""
op.py - Generic editing operations named independently of editor
         commands or buffer methods.  So display editor window code
         etc. needn't depend on a particular editor program or buffer
         class.
"""

from enum import Enum

class Op(Enum):
    'Generic editing operations named independently of editor commands'
    # nop = 0   # Use None for this
    insert = 1  # Buffer methods: insert, also via a i r t y but not c
    delete = 2  # d, also via ed 'c' command
    move = 3    # m
    replace = 4 # c s
    # do these buffer operations belong here?
    create = 4
    destroy = 5

# values for Buffer op attribute, create, destroy apply to whole buffer
# nop, insert, delete, copy, move, replace, create, destroy = range(8)
