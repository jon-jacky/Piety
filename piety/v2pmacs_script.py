# v2pmacs_script.py
#  Run this from Piety directory:  $ python3 -im v2pmacs_script 
from runner import run  # run instead of import to put all identifiers __main__
run('editors/vpm.py') # load Piety editor with viewer panel
run('piety/eventloop.py')  # create piety keyboard event loop, don't start it
run('piety/vpmacs_script.py') # create timer task and its editor buffer
piety_start() # start keyboard event loop and timer task

