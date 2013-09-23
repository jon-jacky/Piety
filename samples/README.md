Piety samples
=============

Piety samples and tests, to run under the Piety scheduler.  For
directions, see the docstrings in each module.  Modules are listed in
the order they were written.

- **path**, put the *piety* directory on the *PYTHONPATH*, see
    directions in the *test* module docstrings.

- **writer**, write to files to demonstrate interleaving concurrency

- **test_writers**, demonstrate *writer* with two concurrent *Writer* instances

- **test_terminal**, test the *terminal* module

- **test_console_blocking**, test the *console* module without the scheduler

- **test_console**, test the *console* module running alone under the scheduler

- **test_console_writers**, test *console* running under the scheduler
    concurrently with two writers.

- **test_shell**, test the Piety Python shell running alone under the scheduler

- **test_shell_writers**, test Python shell under the scheduler
    concurrently with two writers.
