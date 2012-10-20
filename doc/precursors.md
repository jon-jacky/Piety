**Piety** is a notional operating system to be written in Python.  It
is a response to this impulse:

> *Today's operating systems and applications are bloated and
> complicated.  Let's start over, and create a complete system that is
> small, easy to understand, and fun to program.  And, let's build it
> all in our favorite language!*

This seductive idea recurs among each generation of programmers.  It
has inspired some interesting experiments and a few influential
systems.  Alan Kay explained the rationale
[here](http://www.vpri.org/pdf/m2004001_power.pdf):

> *... in programming there is a widespread first order theory that one
> shouldn't build one's own tools, languages, and especially operating
> systems.  This is true --- an incredible amount of time and energy has
> gone down these ratholes.  On the second hand, if you* **can** *build your
> own tools, languages, and operating systems you* **absolutely should**
> *because the leverage that can be obtained (and often the time not
> wasted in trying to fix other people's not quite right tools) can be
> incredible.*

Here are some examples.

| System | Era | Language | Substrate    | Platform  | Applications, Goals |
| ------ | --- | -------- | -------- | -------   | ------- |
| [MCP](http://en.wikipedia.org/wiki/MCP_%28Burroughs_Large_Systems%29), also [here](http://en.wikipedia.org/wiki/Burroughs_large_systems) | 1961-- | Algol (ESPOL) | Bare machine | Burroughs B5000 | Data processing |
| [Unix](http://cm.bell-labs.com/cm/cs/who/dmr/hist.html), also [here](http://genius.cat-v.org/ken-thompson/interviews/unix-and-beyond)  | 1969 -- | C | Bare machine | PDP 7, PDP 11, ... | Programming, Document preparation  |
| [Smalltalk](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls78.html), also [here](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls81.html) and [here](http://propella.sakura.ne.jp/earlyHistoryST/EarlyHistoryST.html) and [here](http://www.vpri.org/pdf/m2004001_power.pdf) and [here](http://news.ycombinator.com/item?id=4229788) | 1970s | Smalltalk | Bare machine | Xerox Alto, ... (purpose-built) | Education |
| [Lisp Machines](http://en.wikipedia.org/wiki/Lisp_machine), also [here](http://www.ugcs.caltech.edu/~weel/lispm.php) and [here](http://www.andromeda.com/people/ddyer/lisp/) and [here](http://www.ugcs.caltech.edu/~weel/lispm/genera-concepts.pdf) | 1970s, 80s | Lisp | Bare machine | MIT CONS, Symbolics, LMI, ... (purpose-built)| Artificial Intelligence |
| Oberon | late 1980s | Oberon | Bare machine | ETH Ceres, ... (NS32032 processor) | Programming, Electronics CAD|
| [Plan 9](http://plan9.bell-labs.com/sys/doc/9.html), also [here](http://doc.cat-v.org/plan_9/) | late 1980s -- | C, Alef | Bare machine | various | Programming, Electronics CAD |
|  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/) | 1997 -- | C | Bare machine | x86, StrongArm, various | OS components |
| ["Scheme Machine"](http://lists.tunes.org/archives/lispos/1998-December/002514.html) | 1998 | Scheme (MzScheme) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | "For now, it's just fun" |
| [ML/OS](http://dspace.mit.edu/bitstream/handle/1721.1/47545/40495469.pdf), also [here](http://www.cs.utah.edu/flux/papers/oskit-sosp97.html) | 1997 | ML (SML/NJ) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | |
| [Squeak](http://www.squeak.org/), also [here](http://ftp.squeak.org/docs/OOPSLA.Squeak.html) | 1997 -- | Smalltalk | Sandbox | various | "development environment in which to build educational software"  |
| [JNode](http://www.jnode.org/) | 2003 -- | Java | Bare machine | | |
| [hOp, House](http://programatica.cs.pdx.edu/House/) | 2004 -- | Haskell | Bare Machine | x86 | "more secure and more reliable software systems" | 
| [HaLVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), also [here](https://github.com/GaloisInc/HaLVM), and [HaNS](http://www.haskell.org/pipermail/haskell-cafe/2011-May/092291.html) | 2010 -- | Haskell | Virtual Machine | Xen hypervisor | "experimental network services" |
| [Mirage](http://www.openmirage.org/), also [here](http://www.openmirage.org/wiki/papers) and [here](http://dl.acm.org/citation.cfm?id=1863114)| 2006 -- | O'Caml | Virtual Machine | Xen hypervisor | "I/O intensive cloud services ... minimize cost of cloud resources" |
| [STEPS]( http://vpri.org/html/work/ifnct.htm), also [here](http://www.vpri.org/pdf/tr2011004_steps11.pdf) and [here](http://news.ycombinator.com/item?id=3996209) | 2006 -- |  OMeta, Nile, Maru, Nothing, ... "Problem-oriented languages" | Bare machine |  various | "recreating (personal computing) ... in less than 1/1000 the amount of program code" | 
| [movitz](http://common-lisp.net/project/movitz/) | 2004 -- | Lisp (CL) |  Bare Machine | x86 | "development platform for operating system kernels, embedded, and single-purpose applications" |
| [Gracle](gracle_excerpts.txt) | 2004 -- | Lisp (CL) | Native OS | Linux | "development and deployment environment" | 
| [LOSAK](http://losak.sourceforge.net/) | 2004 -- | Lisp (LOSAK) | Bare Machine | | |
| [Singularity](http://research.microsoft.com/en-us/projects/singularity/) | 2004 -- | C# | Bare machine | x86 | "more reliable systems and applications" | 
| [Cosmos](http://cosmos.codeplex.com/) | 2007 -- | C# | Bare machine | x86 | OS components |
| [Khoros](http://outofhanwell.wordpress.com/2008/08/16/khoros-a-lua-operating-system/), [lv0](http://lv0.org/), also [here](http://lua-users.org/lists/lua-l/2011-08/msg01189.html) | 2008 -- | Lua | Bare Machine | ||
| [LuaOs](http://luaos.net/docs/manual.php), [SafeLua](http://luaos.net/docs/safelua-api.html) | 2011 -- | Lua (SafeLua) | Bare Machine, Native OS, Sandbox |  Linux || 
| [Lively Kernel](http://www.svgopen.org/2008/papers/93-The_Lively_Kernel_Web_Application_Framework/), also [here](http://www.lively-kernel.org/)  | 2008 -- | Javascript | Sandbox | Web browser | "An IDE ... self-supporting ... inside the browser without any external tools" |
|[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html) | 2009 -- | C | Bare machine | x86 | OS components, used in Stanford [CS140](http://www.scs.stanford.edu/12au-cs140/) OS course |
| [Python-on-a-Chip, PyMite VM](http://code.google.com/p/python-on-a-chip/)  | 2000 -- | Python | Bare machine | PIC, ARM, Arduino, ... microcontrollers | Embedded controllers |
| [Cleese](https://github.com/jtauber/cleese/), also [here](http://code.google.com/p/cleese/) | 2003, 2009 | Python | Bare machine | x86 | "microkernel mostly based on the Python VM and all other OS functionality written Python" |
| [Unununium](http://mail.python.org/pipermail/python-announce-list/2004-July/003220.html), also [here](http://web.archive.org/web/20061013010205/http://www.unununium.org/) | 2004 -- 2006 | Python | OS components, then Native OS |  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), then Linux | "create a better computing environment by maximizing interconnection between components" |
| [Sugar](http://www.ibm.com/developerworks/linux/tutorials/l-sugarpy/), also [here](http://wiki.laptop.org/go/Sugar_Architecture) and [here](http://wiki.laptop.org/go/Understanding_Sugar_code) | 2007 -- | Python | Native OS | OLPC laptop, Linux + Gtk | Education |
| [Pycorn](http://www.pycorn.org/home) | 2008 -- | Python | Bare machine | Gumstix Verdex board (ARM processor) | "... interpreter-centric OS ... easy to use ... educational ... fun!" |
| [Python OS Project (POP)](http://python-os.info/en/) | 2009 -- | Python | Native OS | Linux | "Dominate desktop OS market!" |

Key to **Substrate** column

* **Bare machine** 
The system includes an operating system kernel written mostly
in the favored language, with only a minimal amount of C or assembler.
The "bare machine" might actually be virtual machine or emulator
such as QEMU.

* **Virtual Machine** Similar to Bare Machine, but the system is
designed from the beginning to be deployed only on VMs.

* **Native OS** The system runs on top of a conventional OS.
Programmers and users working in the favored language can mostly avoid
the conventional OS.

* **Sandbox** The system runs on top of a conventional OS, but in a
self-contained environment where most of the the host's facilities are
not available.  Programmers and users working in the sandbox can only
use the utilities provided in the favored language.

* **OS components** The system runs on a minimal OS built from
components chosen from a collection such as [Flux OSKit](http://www.cs.utah.edu/flux/oskit/),
[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html),
or [Cosmos](http://cosmos.codeplex.com/).

[CS140](http://www.scs.stanford.edu/12au-cs140/): Operating
Systems (Stanford) and [OSDev.org](http://wiki.osdev.org/) have
many pages on creating and experimenting with operating systems.

