"""
runner.py - Define the function run, which runs a script in the __main__ namespace
            without creating a new module.  An alternative to import, uses exec.
            Identifiers assigned in the script appear in the __main__ namespace. 
"""

import sys

main_globals = sys.modules['__main__'].__dict__

def run(filename): 
    'Run script in filename in __main__ namespace without creating a  new module'
    exec(open(filename).read(), main_globals)

