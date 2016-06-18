"""
console-job.py - create, connect Command, Job instances for console application
"""

import command, piety

def console_job(controller=None, prompt='', handler=(lambda: None), 
                do_command=(lambda command: None), startup=(lambda: None), 
                stopped=(lambda command: True), cleanup=(lambda: None)):
    """
    Create, connect Command and Job instances for console application.
    See docstrings in piety and command modules for meanings of arguments.
    """
    console = command.Command(prompt=prompt, handler=handler)
    job = piety.Job(controller=controller, handler=console.handler, 
                    command=console, do_command=do_command,
                    startup=startup, restart=console.restart,
                    stopped=stopped, cleanup=cleanup)
    console.do_command = job.do_command
    console.stopped = (lambda: job.stopped() or job.pre_empted)
    return job, console  # return job first, caller may ignore console
