"""
reload_test.py - Experiment with reloading a module in micropython.

Directions appear by each line of code.
"""

# Variables
try:
    x = 0 # re-initialize this variable to this value on every reload
    _ = y # if y is already defined, this module was already imported 
except: 
    # Execute these lines only the first time this module is loaded (imported).
    # These variables should not be re-initialized when the module is reloaded.
    y = 0
    s = '' 

# Functions

# Do not change this function in the reloaded module.
# Its behavior should stay the saem after reloading.
def f():
    print('This is the initial verision of function f')

# Change the body of this function in the reloaded module.
# Its behavior should change after reloading.
def g():
#    print('This is the initial version of function g')
    print('This is the *revised* version of function g')    
    
# This function should not appear when this module is first imported.
# Uncomment this function and its body to make it appear when reloaded.
def h():
    print('This is the new function h')
