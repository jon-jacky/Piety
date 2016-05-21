"""
piety_writers.py - Uses the Piety scheduler to run the console session with
  three jobs created by console_tasks, concurrently with the two
  writer tasks created by writer_tasks.

See console_tasks header for directions on how to run the console jobs.
Except start ed with con.job.ed not just job.ed etc.
See writer_tasks header for drections on how to observe the writer tasks.
"""

import piety

# Writer tasks in writer_tasks module don't appear explicitly here - 
# they are referenced by the piety.schedule data structure used by piety.run
import writer_tasks
import console_tasks as con

def main():
    'Run the console session and writer tasks concurrently under the event loop'
    # con.job.pysh() runs its startup(), calls pysh.start() sets pysh.running=True
    con.job.pysh() # start the first job, recall pysh is in jobs namespace
    # piety.run() calls its piety.start() which sets eventloop.running=True
    piety.run() # start event loop, until pysh >> exit() triggers piety.stop()

if __name__ == '__main__':
    main()
