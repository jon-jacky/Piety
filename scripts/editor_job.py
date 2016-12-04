"""
editor_job.py - Run Job made from display editor Console in a while loop.
         Just an exercise, no need for Job if there is just one application.
         Contrast to eden.py and run_editor.py
"""

import piety
import eden as editor

job = piety.Job(handler=editor.console.handler,
                startup=(lambda: editor.edsel.startup(c=12)),
                restart=editor.console.restart, 
                cleanup=editor.edsel.cleanup)

editor.console.supervisor = job

def main():
    job() # run job startup and restart
    while (not editor.console.stopped() and 
           editor.console.command.line not in editor.console.job_commands):
        job.handler()

if __name__ == '__main__':
    main()
