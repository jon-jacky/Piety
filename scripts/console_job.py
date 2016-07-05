"""
console_job.py - create, connect Command, Job instances for console application
"""

import command, piety

def console_job(controller=None, prompt='', handler=(lambda: None), 
                do_command=(lambda command: None), startup=(lambda: None), 
                stopped=(lambda command: True), cleanup=(lambda: None)):
    """
    Create, connect Command and Job instances for console application.
    See docstrings in piety and command modules for meanings of arguments.
    """
    console = command.Command(prompt=prompt, handler=handler, 
                              do_command=do_command, stopped=stopped)
    job = piety.Job(controller=controller, handler=console.handler, 
                    startup=startup, restart=console.restart,
                    cleanup=cleanup)
    # assign callbacks
    console.job = job # so console can say self.job.pre_empted
    console.do_stop = job.do_stop
    return job, console  # return job first, caller might ignore console
