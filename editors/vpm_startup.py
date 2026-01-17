# vpm_startup.ph invoked from vpm.py   Assumes Piety is current directory
import pmacs, edsel as fr
fr.e('editors/welcome.md') # assumes we are in Piety directory 
pmacs.pm()    # start display editing in viewer window
###N()     # list buffers in viewer window
###oe()   # switch focus back to editor window

