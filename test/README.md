Piety tests
===========

Tests for modules in *Piety/bin* and *Piety/samples* (there may be
more tests in those directories).  For directions, see the docstrings
in each module.  Modules are listed in the order they were written.

- **test_terminal**, test the *terminal* module

- **test_console_blocking**, test the *console* module without the scheduler

- **test_console**, test the *console* module running alone under the scheduler

- **test_console_writers**, test *console* running under the scheduler
    concurrently with two writers.

- **test_shell**, test the Piety Python shell running alone under the scheduler

- **test_shell_writers**, test Python shell under the scheduler
    concurrently with two writers.
