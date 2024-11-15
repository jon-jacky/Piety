
Python on a bare machine
========================

I hope someday to run [Piety](../README.md) on a bare machine with no other
operating system, but only a Python interpreter with minimal support.
I have researched several approaches:

[Hardware Requirements](#Hardware-Requirements)  
[Software Requirements](#Software-Requirements)  
[Software Goals](#Software-Goals)  
[Porting Python](#Porting-Python)  
[Linux](#Linux)  
[Unikernel](#Unikernel)  
[UEFI](#UEFI)  
[NopSys](#NopSys)  
[MicroPython](#MicroPython)  
[Raspberry Pi](#Raspberry-Pi)  
[Tulip Creative Computer](#Tulip-Creative-Computer)  
[Conclusions](#Conclusions)  

## Hardware Requirements ##

I want to run Piety on a self-contained personal computer.  It must not
need another computer or terminal to use it; it must include its own
keyboard and display.

I want to experiment with lots of data in memory, so the computer must
have enough to store hundreds of pages of text (documents, program
source, and web pages) and enough processor power to run the programs to
use them (text editors, interperters/compilers, web browsers).

## Software Requirements ##

I want to run Piety as the complete standalone software system on the
personal computer,  running directly on the hardware, without needing to
run in a virtual machine or container hosted by another operating system.

## Software Goals ##

Piety should be able to  use the Python REPL to inspect and
manipulate any data in the running system, including operating system data
structures and device registers.

Piety should be self-hosted: once it has reached a barely
usable state, further development of the Piety system should be done  on
the personal computer by using Piety itself.   

Self-hosting is a reasonable goal for developing Piety software in Python.
But getting the Python interpreter itself running on a bare machine may
require programming languages and tools not included in Piety.

## Porting Python ##

A Python interpreter must be adapted, or *ported*, to any environment
where it runs.  That environment is usually a conventional operating
system, but it can be nothing more than a minimal connection to the
machine's hardware, as in *NopSys* and *MicroPython* (below).

*Porting* is a [software development
project](https://devguide.python.org/porting/) whose product is called a
*port*.  Ports for popular operating systems are available from various
sources including [python.org](https://www.python.org/downloads/).

The usual Python interpreter is CPython, which is a program written in C.
The alternative MicroPython interpreter is also written in C. To port an
interpreter, you have to modify (edit) some of the interpreter's C source
files, then compile them and link them with files for the target
environment, all using C language development tools.

## Linux ##

Linux is an open-source Unix-like operating system which is available for
almost any personal computer.   There are vast resources in print and
online that explain everything about it at any level of detail.   It hosts
development tools for almost every programming language.   It provides
great flexibility for creating custom configurations.

It is possible to configure a minimal Linux system that runs the Python
interpreter as its process 1 and boots to the Python prompt.  For example,
[Snakeware](https://github.com/joshiemoore/snakeware)  (also at
[YouTube](https://www.youtube.com/watch?v=Zy8NXuzBPhA)  and
[HN](https://news.ycombinator.com/item?id=23391380)) does just that.
It uses an existing Python port to Linux, so no porting effort is needed.

Any such Python on Linux system still uses a Linux kernel, with  device
drivers, file system, etc. all written in C.   The Linux operating system
is opaque  to Python; you can't inspect it or control it through the
Python REPL. So this configuration does not achieve the goal of an almost
all-Python system.   But it is a good start; the user and the application
programmer only see the Python part.

## Unikernel ## 

A [unikernel](https://en.wikipedia.org/wiki/Unikernel) comprises a single
application combined with just enough of an operating system to support
it, which can run on a bare machine or virtual machine without a
conventional operating system.  The movitivation is to make a small,
efficient, and secure system by eliminating all the machinery not needed
by that one  application, such as a shell and processes, and retaining
only the essential device drivers, etc.  Unikernels are sometimes built
from device drivers and other fragments taken from conventional operating
systems such as Linux or one of the BSDs.

Unikernels are usually considered as alternatives to conventional
virtual machines or containers for running network applications on
virtual machine hosts in the cloud. Here is a
[review](https://github.com/cetic/unikernels) and an extensive [reading
list](https://github.com/papers-we-love/papers-we-love/tree/master/unikernels)
and a recent [discussion](https://news.ycombinator.com/item?id=30247022).

It seems one might build a Unikernel where the single application is the
Python interpreter itself. Any Python modules could be loaded into the
interpreter without extending that Unikernel. There are already
unikernels specialized for running applications in a single language:
[MirageOS](https://mirage.io/) for OCaml and
[HalVM](https://galois.com/project/halvm/) for Haskell.

Several years ago I was encouraged by this
[report](http://blog.netbsd.org/tnf/entry/an_internet_ready_os_from)
to try an
[experiment](https://github.com/jon-jacky/Piety/tree/master/unikernel) 
with a system called
[Rump Kernel](https://github.com/rumpkernel/wiki/wiki)
to make a unikernel from the CPython interpreter and parts of the NetBSD
operating system.  I got as far as booting my unikernel on the QEMU
virtual machine monitor, only to find that it could not read from the 
keyboard.  I submitted an
[issue](https://github.com/rumpkernel/rumprun/issues/64)
but the Rump Kernel project became inactive before it could be fixed.

## UEFI ## 

[UEFI](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface
) is software built into the nonvolatile memory of most modern x86
computers.  It is used during startup (boot) before the computer's usual
operating system is loaded. (It replaces the simpler BIOS found on older
computers.) UEFI is actually an operating system in its own right, which
accesses the computer's hardware and file system and can provide a shell
(command interpreter) that can load and run programs. Source code for a
reference UEFI implementation named
[TianoCore](https://www.tianocore.org/) is available. You can write
programs that run on UEFI without another operating system (see
[here](https://wiki.osdev.org/UEFI), also
[here](http://x86asm.net/articles/uefi-programming-first-steps/)).

It seems it might be possible to run just Python on the built-in UEFI
on an otherwise bare machine.  

In fact, Python has been ported to run on UEFI without a conventional
operating system. These ports were created to run Python scripts that
test UEFI itself; they were not intended for general-purpose Python
programming. A port of Python version 3.6.8 is discussed [here](https://
chipsec.github.io/installation/USB%20with%20UEFI%20Shell.html).. A port
of MicroPython is discussed [here](https://www.intel.com/content/www/us/
en/developer/articles/technical/implementing-micropython-as-a-uefi-test-
framework.html) and [here](https://github.com/tianocore/edk2-
staging/tree/MicroPythonTestFramework/MicroPythonPkg). An earlier
project ported Python to the GRUB bootloader to test the BIOS, see
[here](https://biosbits.org/),
[here](https://us.pycon.org/2015/schedule/presentation/378/),
[here](https://news.ycombinator.com/item?id=9453677), and
[here](https://www.youtube.com/watch?v=36QIepyUuhg). 

It seems that UEFI
ought to be a lot simpler that Linux, but it is not. One
developer [observes](https://news.ycombinator.com/item?id=24888307) "my
mobo's UEFI is typically larger than the kernel it runs." Another
developer 
[comments](https://www.reddit.com/r/linuxquestions/comments/63
azo4/eli5_what_exactly_is_the_problem_with_uefi_and/) 
"It's about 10% the size of the Linux kernel; and if you exclude Linux's
device drivers it's actually bigger than the Linux kernel."

And, it is not simple to set up or use. In contrast to Linux,
explanations of UEFI are fragmented and often confusing. It can be
difficult even to find out what UEFI features are provided on a
particular computer, or how to access them ("Does the UEFI shell work on
this machine?" etc.).

## NopSys ## 

[NopSys](https://github.com/nopsys/nopsys) ("No Operating System") is an
attempt to provide the minimum amount of low-level code needed to support
an operating system written in a high-level language.  It was used to
build [CogNOS](https://github.com/nopsys/CogNOS) (also
[here](https://github.com/nopsys/SmalltalkNOS) and
[here](https://charig.github.io/assets/papers/SCDE-DLS.pdf)), a standalone
Smalltalk language system that runs on a bare machine.   Among all the
[projects I surveyed](precursors.md),  this one appears closest to my
goals for Piety.

NopSys is not an operating system.  It is only  a bootloader, and some
event handlers that perform the essential register management required by
the hardware before handing off the event to the high level language. 
NopSys is for x86 hardware, and comprises 3428 lines of C and 608 lines
of assembler.

The Cog virtual machine (for the Smalltalk language) was ported to NopSys
by adding methods for reading and writing CPU control registers,
interacting with hardware I/O ports, reading a timer, and connecting to an
interrupt handler. The CogNos operating system, including
[interrupt handlers, device drivers and the file system](https://github.com/nopsys/SmalltalkNOS), 
is written in Smalltalk.

NopSys is supposed to be language-independent -- the authors write  "we're
eager to see people create PyNOS, RubyNos, etc." -- but has only been used
to build CogNos.  CogNos was able to run some tests and performance
experiments, but (the authors write) "there  would certainly be much more
work needed before one could consider deploying our system." The project
apparently became inactive before that happened.

## MicroPython ## 

[MicroPython](http://micropython.org/) is a Python implementation designed
to run without an operating system on small microcontrollers, to be
embedded in electronics projects.  It is a new implementation with an
entirely different codebase than the usual CPython interpreter.

MicroPython has some interesting differences from CPython.   It can
compile to native machine code instead of bytecodes for an interpreter.
You can write inline assembler code in the Python source. However some
Python language features might not be included, and many Python standard
library modules are not available. There is a port of MicroPython
that runs on Unix-like operating systems so you  can evaluate the language
on an ordinary computer.

MicroPython is not self-hosted. You edit MicroPython modules on a larger
computer with a conventional operating system, use a development system
to build them (and possibly some C modules also) into a memory image,
then download that image to flash memory on the microcontroller, where
the MicroPython interpreter/compiler executes it. MicroPython can
provide a command line with a Python REPL on the microcontroller, but it
communicates over a serial port so you need a terminal or another
computer to use it. The MicroPython software includes tools that run on
the host for building downloadable software images, and other host tools
for interacting with the software running on the microcontroller.

MicroPython does provide Python running on a bare machine.  But the
microcontrollers that MicroPython was created for are much smaller and
slower than the processor in a modern personal computer, and do not include
any disks or other mass storage, but only non-volatile flash memory for
program storage and some RAM for storing the variables of running
programs. The *pyboard*, a small single-board computer designed to run
MicroPython, has an ARM Cortex M4 CPU running at 168 MHz, with 1024KiB
flash ROM and 192KiB RAM.

MicroPython and the pyboard appeared in 2013. The following sections
describe some recent, more powerful microcontroller products that
support MicroPython and might be able to run some version of Piety.

## Raspberry Pi ## 

Raspberry Pi is a family of small, low-cost single-board computers
intended for education and hobby projects.  Unlike most personal
computers, they have an ARM processor (not x86) and use an unusual boot
(startup) method that does not use BIOS or UEFI.   To use an RPi as a
personal computer you must add a power supply, keyboard, and display.
They are somewhat slower and have less memory and mass storage than most
modern personal computers, but they are still usable (many experiences
are reported [here](https://news.ycombinator.com/item?id=31191817)).

The Raspberry Pi provides an accessible path into low-level programming.
Many tutorials including university courses teach how to write a simple
operating system from scratch on the Raspberry Pi, in
[assembler](https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/os/),
[C](http://web.stanford.edu/class/cs140e/), or even
[Rust](https://downey.io/blog/cs140e-writing-an-operating-system-in-rust).
Perhaps the Python interpreter could be ported to some of these.

[Circle](https://github.com/rsta2/circle) is a C++ "bare metal programming
environment for the Raspberry Pi", for building C++ programs that run  on
the RPi without an operating system, for example this [music
synthesizer](https://github.com/probonopd/MiniDexed)
Most of the code in its Github repository is C, not C++.
Perhaps the Python interpreter could be ported to it.
There is already a Smalltalk port to the Pi that uses Circle
[here](https://github.com/michaelengel/crosstalk)
(discussed [here](https://news.ycombinator.com/item?id=23874206#23883895)).

A Raspberry Pi can run a purpose-built Linux such as *Raspbian*,
so it can be treated like a variant of the Linux systems described
in a preceding section.
For example, [PiratePython](https://github.com/pimoroni/PiratePython)
(also at [HN](https://news.ycombinator.com/item?id=16180975)) is a
*Raspbian* build configured to run Python applications.  It uses
an existing Python port to Linux.

An early experiment with porting MicroPython  to the Raspberry Pi Zero
(ARM 11 at 1 GHz, 512MB RAM) is described
[here](https://www.snaums.de/static/resources/2017-12-mpy.pdf). It got as
far as blinking an LED connected to one of the Pi GPIO pins, but
apparently does not support any of the other hardware.

There is a port of the 
[Circuit Python](https://docs.circuitpython.org/en/latest/README.html)
fork of MicroPython to several Raspberry Pi models,
decribed [here](https://learn.adafruit.com/circuitpython-on-raspberry-pi-bare-metal-no-os).   The 
[release notes](https://github.com/adafruit/circuitpython/releases/tag/7.3.0-beta.2) 
(Apr 2022) say this port is "considered alpha and
will have bugs and missing functionality", but there is already a
[manual](https://cdn-learn.adafruit.com/downloads/pdf/circuitpython-on-raspberry-pi-bare-metal-no-os.pdf) 
available. It supports the Pi HDMI (video) port and has been used to
drive an 
[e-ink display](https://blog.adafruit.com/2021/11/02/bare-metal-circuitpython-on-a-raspberry-pi-hdmi-and-e-ink/). 
The *Adafruit* company, the project sponsor, wrote in 2022, "One of the
plans is to make a little computer with a keyboard, that is just
CircuitPython." (At this writing, Nov 2024, so such product has been
announced).
 
## Tulip Creative Computer ##

The [Tulip Creative Computer](https://github.com/shorepine/tulipcc) 
is a small self-contained computer based on the ESP32-S3 microcontroller
running MicroPython. It includes a built-in color touch-screen display
and a USB port for connecting a keyboard. It is intended to be used as a
music synthesizer, and comes with several MicroPython programs for music
synthesis and creating color graphics.

The Tulip is the nearest thing we have seen to our vision for a Piety
personal computer.   It doesn't quite qualify because the display is
too small, only about 4 by 6 inches (but see below), and, like other
MicroPython systems, software development is not self-hosted, but
requires another computer.
 
Instead of purchasing the Tulip with the small built-in display, 
you can  
[build one yourself](https://github.com/shorepine/tulipcc/blob/main/docs/tulip_build.md)
in various configurations, following directions from the designers. 
[One configuration](https://github.com/shorepine/tulipcc/blob/main/docs/tulip_breadboard.md)
uses an [ESB32-S3 development board](https://www.adafruit.com/product/5364)
and a 10.1" display.  The development board has similar components as
the prebuilt Tulip including 32MB of flash and 8MB of RAM
and runs at 240 MHz.

The 
[MicroPython port to ESP32](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md)
uses the microcontroller vendor's ESP-IDF build tool.  ESP-IDF builds 
software that includes the FreeRTOS real-time operating system.  MicroPython
runs as a task under FreeRTOS.

## Conclusions ##

The obvious first step to running Python on a bare machine is to
configure a minimal Linux running Python as its process 1. It is just a
configuration and building task, not a programming project. It uses an
existing Python port and there are already example Linux configurations
to copy or imitate.

This would provide a system that boots into a Python prompt and provides
a Python-only system to the user and application programmer.  This is all
we need to perform the essential experiment to see if it is
feasible to continue Piety development and other personal computing
activities using only Python running Piety in the console, without
depending on a host OS to provide a desktop with multiple windows,
shells, and other utilities.

Running Python on a unikernel or on UEFI provides no advantages over
Python on Linux. Both include a large amount of opaque non-Python code
with no obvious path to replacing it. Both are likely to be less
convenient to work with than Linux. The value of unikernels and UEFI is
that they are working examples of how to structure a system differently
from a Linux kernel and its processes.

To take the next steps to a Python operating system
on a personal computer, *CogNOS* with *NopSys* shows a way to proceed:
Port CPython to NopSys, using the port of the Cog VM for Smalltalk as a
model. Then, write the rest of the operating system in Python, using the
Smalltalk code for CogNOS as a model. (Instead of using NopSys, we might
extract functionally equivalent software from Linux or some other recent
system). That would be an ambitious and difficult project for me.

A very different kind of project we might take on is to try to get some
version of Piety running in MicroPython on a microcontroller. This
experiment would be to find out if such a small and simple system can
support a pleasant programming environment that is self-contained,
where significant programs can be written without an ongoing connection
to a more powerful host computer. This project would likely include some
hardware work, integrating a microcomputer development board with a
keyboard and display.

Revised Nov 2024

