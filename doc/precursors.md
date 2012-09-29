> *Today's operating systems and applications are bloated and
> complicated.  Let's start over, and create a complete system that is
> small, easy to understand, and fun to program.  And, let's build it
> all in our favorite language!*

This seductive idea recurs among each generation of programmers.  It
has inspired some interesting experiments and a few influential systems.
Here are some examples.

| System | Era | Language | Substrate    | Platform  | Applications |
| ------ | --- | -------- | -------- | -------   | ------- |
| [MCP](http://en.wikipedia.org/wiki/MCP_%28Burroughs_Large_Systems%29), also [here](http://en.wikipedia.org/wiki/Burroughs_large_systems) | 1961-- | Algol (ESPOL) | Bare machine | Burroughs B5000 | Data processing |
| [Unix](http://cm.bell-labs.com/cm/cs/who/dmr/hist.html)  | 1969 -- | C | Bare machine | PDP 7, PDP 11, ... | Programming<br>Document preparation  |
| Smalltalk | 1970s | Smalltalk | Bare machine | Xerox Alto, ...<br>(purpose-built) | Education |
| Lisp Machines | 1970s, 80s | Lisp | Bare machine | Symbolics, LMI, ...<br>(purpose-built)| Artificial Intelligence |
| Oberon | late 1980s | Oberon | Bare machine | ETH Ceres, ...<br>(NS32032 processor) | Programming<br>Electronics CAD|
| [Plan 9](http://plan9.bell-labs.com/sys/doc/9.html), also [here](http://doc.cat-v.org/plan_9/) | late 1980s -- | C, Alef | Bare machine | various | Programming<br>Electronics CAD |
| ["Scheme Machine"](http://lists.tunes.org/archives/lispos/1998-December/002514.html) | 1998 | Scheme (MzScheme) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | |
| [ML/OS](dspace.mit.edu/bitstream/handle/1721.1/47545/40495469.pdf), also [here](http://www.cs.utah.edu/flux/papers/oskit-sosp97.html) | 1997 | ML (SML/NJ) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | |
| Squeak | | Smalltalk | Native OS | various ||
| hOp, House | | Haskell | Bare Machine | x86 || 
| HaLVM, HaNS | | Haskell | Virtual Machine | Xen hypervisor | Cloud computing |
| Mirage | | O'Caml | Virtual Machine | Xen hypervisor | Cloud computing |
| [STEPS]( http://vpri.org/html/work/ifnct.htm), also [here](http://www.vpri.org/pdf/tr2011004_steps11.pdf) and [here](http://news.ycombinator.com/item?id=3996209) | 2006 -- |  OMeta, Nile, Maru, Nothing, ...<br>"Problem-oriented languages" | Bare machine |  various | Education<br>"Desktop publishing" | 
| [movitz](http://common-lisp.net/project/movitz/) | 2004 -- | Lisp (CL) |  Bare Machine | x86 | |
| Gracle | 2004 -- | Lisp (CL) | Native OS | Linux || 
| [LOSAK](http://losak.sourceforge.net/) | 2004 -- | Lisp (LOSAK) | Bare Machine | | |
| Khoros, [lv0](http://lv0.org/) | 2004 -- | Lua | Bare Machine | ||
| LuaOs, SafeLua | 2004 -- | Lua | | || 
| [Lively Kernel](http://www.svgopen.org/2008/papers/93-The_Lively_Kernel_Web_Application_Framework/) also [here](http://www.lively-kernel.org/)  | 2008 -- | Javascript | Sandbox | Web browser ||
| [Sugar](http://www.ibm.com/developerworks/linux/tutorials/l-sugarpy/), also [here](http://wiki.laptop.org/go/Sugar_Architecture) and [here](http://wiki.laptop.org/go/Understanding_Sugar_code) | 2007 -- | Python | Native OS | OLPC laptop<br>Linux + Gtk | Education |
| [Cleese](https://github.com/jtauber/cleese/) | 2003 --| Python | Bare machine |||
| [Pycorn](http://www.pycorn.org/home) | 2008 -- | Python | Bare machine | Gumstix Verdex board<br>(ARM processor) | Education |
| [Python OS Project (POP)](http://python-os/en/) | 2009 -- | Python | Native OS | Linux | Desktop OS<br>"Just For Fun" |

Key to Substrate column

Bare machine 
: The system includes an operating system kernel written
in the favored language, and (usually) a bit of C or assembler.
The "bare machine" might actually be virtual machine or emulator
such as QEMU.

Virtual Machine
: Similar to Bare Machine, but the system is designed from the
beginning to be deployed only on VMs

Native OS 
: The system runs on top of a conventional OS, whose facilities are
all available.  The system provides an environment where programmers
and users can avoid utilities not written in the favored language.

Sandbox
: The system runs on top of a conventional OS in a "sandbox" where
most of the the host's facilities are not available.  Programmers and
users can only use the utilities provided in the favored language.

OS components
: The system runs on a minimal OS built from components, for example
[Flux OSKit](http://www.cs.utah.edu/flux/oskit/) or
[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html).
