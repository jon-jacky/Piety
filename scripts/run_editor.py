"""
run_editor.py- Run Task made from display editor Console with Piety event loop.
  Just an exercise, no need for Piety if there is just one application.
  This long-winded module demonstrates the motivation for the Job class.
  Contrast to desoto.py and editor_job.py
"""

import sys, piety  
import desoto as editor

task = piety.Task(name='editor',handler=editor.console.handler,input=sys.stdin)

# Enable editor.console to call piety.stop without using piety.Job class
class Stopper():
    def __init__(self):
        self.replaced = False # must be here, but never used
    def stop(self):
        piety.stop()

# At exit, editor.console calls supervisor.stop, which calls piety.stop
editor.console.supervisor = Stopper()  

def main():
    editor.edsel.ed.quit = False # previous quit might have set it True
    editor.edsel.startup(c=12)
    editor.console.restart()
    piety.run()
    editor.console.restore()
    editor.edsel.cleanup()

if __name__ == '__main__':
    main()
