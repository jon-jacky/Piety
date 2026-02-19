
bin
===

Shell scripts that configure Piety on Unix-like platforms.

Put this directory on your execution *PATH*.  Or, install its contents
in some directory that is on your *PATH* (for details, see *paths* in
this directory).
 
Some files in this directory are copies of files stored elsewhere,
that configure Piety at system boot, or when a particular user logs in.

- **.profile** - Put this file in your home directory to set the
*PYTHONPATH*, cd to your ~/Piety directory, start Python, and run the
*vpm* startup module when you log into a console terminal -- BUT NOT
when you log into the graphical desktop. Note that this file's name
starts with a dot, so you must use the *-a* option to see it when you
run an *ls* command.
 
- **override.conf** - Put this file in the directory
*/etc/systemd/system/getty@tty1.service.d* to cause the system to
autologin user *jon* when the system boots. This has been tested on
Debian Linux that has been configured to boot into *multi-user.target*
 
- **paths**: assigns paths for running Piety on a Unix-like host with
  a VT-100 compatible terminal.

- **systemd.txt**: *systemd* commands for configuring and execuing boot.

Revised Feb 2026

