"""
console_line_tasks.py - Create Piety console jobs, session used by piety_line.twisted
"""
import sys # for sys.stdin
import piety, session, job, commandline
import pysh, ed, edd as _edd # rename edd module so we can use edd as job name

class Namespace(object): pass # another way to avoid name clashes
jobs = Namespace()

# Session, a terminal task
console = session.Session(name='console', event=sys.stdin)

# Python shell

def pysh_startup():
    pysh.pexit = False # enable pysh event loop, compare to Job stopped= below

# Name the command pyshc to avoid name clash with pysh module
# Remove trailing blank from prompt, raw_input adds its own trailing blank
pyshc = commandline.CommandLine(prompt='>> ', handler=pysh.mk_shell())

# Put pysh job in the jobs namespace to avoid name clash with pysh module
# stopped=... enables exit on exit() command or ^D
jobs.pysh = job.Job(session=console, application=pyshc, startup=pysh_startup, 
                    stopped=(lambda: pysh.pexit))

# line editor

# startup function handles optional filename argument and optional keyword arg.
def ed_startup(*filename, **options):
    if filename:
        ed.e(filename[0])
    if 'p' in options:
        edc.application.prompt = options['p'] 
    ed.quit = False # enable event loop, compare to Job( stopped=...) arg below

# Name the job edc to avoid name clash with ed module.
# Exit with q only, ^D exit is not enabled
edc = job.Job(session=console,
              application=commandline.CommandLine(prompt='', handler=ed.cmd),
              startup=ed_startup, stopped=(lambda: ed.quit))
              
# display editor

# startup function handles optional filename argument and optional keyword arg.
def edd_startup(*filename, **options):
    _edd.ed.quit = False # enable event loop, compare to Job( stopped=..) arg below
    if 'p' in options:
        edd.application.prompt = options['p'] #edd *not* _edd, Piety command object
    _edd.init_display(*filename, **options) # _ed.prompt is not used by Piety

# edd module was imported as _edd so we can call the job edd without name clash
edd = job.Job(session=console, 
              application=
              commandline.CommandLine(prompt='', handler=_edd.cmd),
              startup=edd_startup, 
              cleanup=_edd.restore_display)

# Enable exit with q, must use separate statement so application has a name
edd.stopped=(lambda: _edd.ed.quit)

# Make edd.main an alias for edd.__call__ so we can call edd.main(...) using
#  exactly the same syntax as when we import edd.py into Python without Piety
edd.main = edd.__call__
