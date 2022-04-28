
Python on a bare machine
========================

I hope someday to run [Piety](../README.md) on a bare machine with no other
operating system, but only a Python interpreter with minimal support.
I have researched several approaches:

[Hardware Requirements](#Hardware-Requirements)  
[Software Requirements](#Software-Requirements)  
[Linux](#Linux)  
[NopSys](#NopSys)  
[Raspberry Pi](#Raspberry-Pi)  
[MicroPython](#MicroPython)  
[UEFI](#UEFI)  
[Unikernel](#Unikernel)  
[Conclusions](#Conclusions)  

## Hardware Requirements ##

I want to run Piety on a self-contained personal computer.  It must not
need another computer or terminal to use it; it must include its own
keyboard and display.

It must have enough memory to store thousands of pages of text (documents,
program source, and web pages) and enough processor power to run the
programs to use them (text editors, interperters/compilers, web browsers).

## Software Requirements ##

I want to run Piety as the complete standalone software system on the
personal computer,  running directly on the hardware, without needing to
run in a virtual machine or container hosted by another operating system.

The goal is for Piety to be self-hosted: once it has reached a barely
usable state, further development of the Piety system should be done 
on the personal computer by using Piety itself.  

Recall that Piety is an all-Python system; Python is the only available
programming language. So self-hosting is a reasonable goal for developing
Piety software in Python.  BUT developing the support to run the Python
interpreter itself on the bare machine cannot be self-hosted on the all-
Python Piety system, because this will require working with code in C and
maybe even assembler. That will require the development tools for those
languages as well.

## Linux ##

Linux is an open-source Unix-like operating system which is available for
almost any personal computer.   There are vast resources in print and
online that explain everything about it at any level of detail.   It hosts
development tools for almost every programming language.   It provides
great flexibility for creating custom configurations.

It is possible to configure a minimal Linux system that runs the Python
interpreter as process 1 and boots to the Python prompt.  For example,
[Snakeware](https://github.com/joshiemoore/snakeware)  (also at
[YouTube](https://www.youtube.com/watch?v=Zy8NXuzBPhA)  and
[HN](https://news.ycombinator.com/item?id=23391380)) does just that.

Any such Python on Linux system still uses a Linux kernel, with device
drivers, file system, etc. all written in C.  So it does not achieve the
goal of an almost all-Python system -- although the user and the
application programmer only see the Python part. 

## NopSys ## 

To come ...

## Raspberry Pi ## 

Raspberry Pi is a family of small, low-cost single-board computers
intended for education and hobby projects.  Unlike most personal
computers, they have an ARM processor (not x86) and use an unusual boot
(startup) method that does not use BIOS or UEFI.   To use an RPi as a
personal computer you must add a power supply, keyboard, and display.
They are somewhat slower and have less memory and mass storage than most
modern personal computers, but they are still usable.

The Raspberry Pi provides an accessible path into low-level programming.
Many tutorials including university courses teach how to write a simple
operating system from scratch on the Raspberry Pi, in
[assembler](https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/os/),
[C](http://web.stanford.edu/class/cs140e/), or even
[Rust](https://downey.io/blog/cs140e-writing-an-operating-system-in-rust).
Perhaps some of these might be adapted for running a Python interpreter.

[Circle](https://github.com/rsta2/circle) is a C++ "bare metal programming
environment for the Raspberry Pi", for building C++ programs that run  on
the RPi without an operating system, for example this [music
synthesizer](https://github.com/probonopd/MiniDexed)  Perhaps it could be
adapted to run the CPython interpreter.  Most of the code in its Github
repository is C, not C++.

A Raspberry Pi can run a purpose-built Linux such as *Raspbian*,
so it can be treated like a variant of the Linux systems described
in the preceding section.
For example, [PiratePython](https://github.com/pimoroni/PiratePython)
(also at [HN](https://news.ycombinator.com/item?id=16180975)) is a
*Raspbian* build configured to run Python applications.

## MicroPython ## 

[MicroPython](http://micropython.org/) is a Python implementation designed
to run without an operating system on small microcontrollers, to be
embedded in electronics projects.  It is a new implementation with an
entirely different codebase than the usual CPython interpreter.

MicroPython has some interesting differences from CPython.   It can
compile to native machine code instead of bytecodes for an interpreter.
You can write inline assembler code in the Python source. However some
Python language features might not be included, and many Python standard
library modules are not available. There are  versions  of MicroPython
that run on Unix-like operating systems so you  can evaluate the language
on an ordinary computer.

MicroPython is not self-hosted.  You edit MicroPython code on a larger
computer with a conventional operating system, then download it to the
microcontroller, where the MicroPython interpreter/compiler executes it.
MicroPython can provide a command line with a Python REPL on the
microcontroller, but it communicates over a serial port so you need a
terminal or another computer to use it.

MicroPython provides Python running on a bare machine.  But the
microcontrollers that MicroPython is written for are much smaller and
slower than the processor in a modern personal computer.  The *pyboard*, a
small single-board computer designed to run MicroPython, has an ARM Cortex
M4 CPU running at 168 MHz, with 1024KiB flash ROM and 192KiB RAM.
MicroPython has been ported to  other microcontroller boards with similar
resources, including the Raspberry Pi Pico (ARM Cortex M0+ 133 MHx, 2MB
Flash  ROM, 264 KiB RAM). 

There is an experiment with porting MicroPython without an operating
system to the larger, faster Raspberry Pi Zero (ARM 11 at 1 GHz, 512MB
RAM) described in detail
[here](https://www.snaums.de/static/resources/2017-12-mpy.pdf). It got as
far as blinking an LED connected to one of the Pi GPIO pins, but
apparently does not support any of the other hardware (display, USB port,
mass storage).

## UEFI ## 

To come ...

## Unikernel ## 

To come ...

## Conclusions ##

The hardware requirements for the Python-powered personal computer are
modest. Almost any personal computer of any age or performance level should
work, even an old netbook, or any of the Raspberry Pi models (except the
Pico).  Small microcontrollers would probably not work, however.

Running Python as process 1 on a minimal Linux looks like the obvious
first step.   It is just a configuration  task, not a development project.
It uses an unmodified Python interpreter and there are already example
Linux configurations to copy or imitate.  And, Linux makes a good platform
for developing  subsequent stages in the Piety project.

NopSys ...

Raspberry Pi ...

MicroPython runs on microcontrollers that are too small to serve as self-
contained personal computers.  Porting MicroPython to a larger computer
would likely take as much work as porting CPython to the same bare
machine, but would only result in a nonstandard implementation with an
incomplete standard library.  And yet ... compilation to native
code and inline assembler code is intriguing.

Running Python on UEFI or a Unikernel seems to provide no advantages over
Python on Linux.  Both include a large amount of non-Python code with no
obvious path to  replacing it.  Both are likely to be less convenient to
work with than Linux. The value of UEFI and Unikernels is that they are
working examples of  how to structure a system differently from a Linux
kernel and its processes.

Revised Apr 2022
