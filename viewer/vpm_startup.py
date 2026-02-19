# vpm_startup.ph invoked from vpm.py   Assumes Piety is current directory
import pmacs, edsel as fr
fr.e('viewer/keys.txt')
fr.e('viewer/viewer.py')
fr.e('viewer/README.md')
fr.e('viewer/desktop.txt') # load this one last, so it appears in viewer
# Put some text in the Python REPL
print("""
>>> # This is the Python interpreter
>>> """)
pmacs.pm()    # start display editing in viewer window
###N()     # list buffers in viewer window
###oe()   # switch focus back to editor window

