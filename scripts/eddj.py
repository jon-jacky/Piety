"""
eddj.py - Run an edd display editor job.
 Use job and key modules instead of Python raw_input to get command line.
 BUT do not use Piety scheduler.
"""

import edd, job, key

eddc = job.Job(prompt='', startup=edd.init_display, 
               handler=edd.cmd, reader=key.Key(),
               cleanup=edd.restore_display) # use default stopcmd='q'

# No other jobs, so leave default suspend=None

def main():
    edd.ed.quit = False # previous quit might have set it True
    eddc()
    while not edd.ed.quit:
        eddc.reader()   # q command sets edd.ed.quit True, forces exit

if __name__ == '__main__':
    main()
