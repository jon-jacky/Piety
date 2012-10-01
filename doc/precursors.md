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

| System | Era | Language | Substrate    | Platform  | Applications |
| ------ | --- | -------- | -------- | -------   | ------- |
| [MCP](http://en.wikipedia.org/wiki/MCP_%28Burroughs_Large_Systems%29), also [here](http://en.wikipedia.org/wiki/Burroughs_large_systems) | 1961-- | Algol (ESPOL) | Bare machine | Burroughs B5000 | Data processing |
| [Unix](http://cm.bell-labs.com/cm/cs/who/dmr/hist.html), also [here](http://genius.cat-v.org/ken-thompson/interviews/unix-and-beyond)  | 1969 -- | C | Bare machine | PDP 7, PDP 11, ... | Programming<br>Document preparation  |
| [Smalltalk](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls78.html), also [here](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls81.html) and [here](http://propella.sakura.ne.jp/earlyHistoryST/EarlyHistoryST.html) and [here](http://www.vpri.org/pdf/m2004001_power.pdf) and [here](http://news.ycombinator.com/item?id=4229788) | 1970s | Smalltalk | Bare machine | Xerox Alto, ...<br>(purpose-built) | Education |
| [Lisp Machines](http://en.wikipedia.org/wiki/Lisp_machine), also [here](http://http://www.ugcs.caltech.edu/~weel/lispm.php) and [here](http://www.andromeda.com/people/ddyer/lisp/) | 1970s, 80s | Lisp | Bare machine | MIT CONS, Symbolics, LMI, ...<br>(purpose-built)| Artificial Intelligence |
| Oberon | late 1980s | Oberon | Bare machine | ETH Ceres, ...<br>(NS32032 processor) | Programming<br>Electronics CAD|
| [Plan 9](http://plan9.bell-labs.com/sys/doc/9.html), also [here](http://doc.cat-v.org/plan_9/) | late 1980s -- | C, Alef | Bare machine | various | Programming<br>Electronics CAD |
| ["Scheme Machine"](http://lists.tunes.org/archives/lispos/1998-December/002514.html) | 1998 | Scheme (MzScheme) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | |
| [ML/OS](http://dspace.mit.edu/bitstream/handle/1721.1/47545/40495469.pdf), also [here](http://www.cs.utah.edu/flux/papers/oskit-sosp97.html) | 1997 | ML (SML/NJ) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | |
| [Squeak](http://www.squeak.org/), also [here](http://ftp.squeak.org/docs/OOPSLA.Squeak.html) | 1997 -- | Smalltalk | Sandbox | various | Education<br>Web applications |
| [hOp, House](http://programatica.cs.pdx.edu/House/) | 2004 -- | Haskell | Bare Machine | x86 || 
| [HaLVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), also [here](https://github.com/GaloisInc/HaLVM), and [HaNS](http://www.haskell.org/pipermail/haskell-cafe/2011-May/092291.html) | 2010 -- | Haskell | Virtual Machine | Xen hypervisor | Cloud computing |
| [Mirage](http://www.openmirage.org/), also [here](http://www.openmirage.org/wiki/papers) and [here](http://dl.acm.org/citation.cfm?id=1863114)| 2006 -- | O'Caml | Virtual Machine | Xen hypervisor | Cloud computing |
| [STEPS]( http://vpri.org/html/work/ifnct.htm), also [here](http://www.vpri.org/pdf/tr2011004_steps11.pdf) and [here](http://news.ycombinator.com/item?id=3996209) | 2006 -- |  OMeta, Nile, Maru, Nothing, ...<br>"Problem-oriented languages" | Bare machine |  various | Education<br>"Desktop publishing" | 
| [movitz](http://common-lisp.net/project/movitz/) | 2004 -- | Lisp (CL) |  Bare Machine | x86 | |
| [Gracle](gracle_excerpts.txt) | 2004 -- | Lisp (CL) | Native OS | Linux || 
| [LOSAK](http://losak.sourceforge.net/) | 2004 -- | Lisp (LOSAK) | Bare Machine | | |
| [Khoros](http://outofhanwell.wordpress.com/2008/08/16/khoros-a-lua-operating-system/), [lv0](http://lv0.org/), also [here](http://lua-users.org/lists/lua-l/2011-08/msg01189.html) | 2008 -- | Lua | Bare Machine | ||
| [LuaOs](http://luaos.net/docs/manual.php), [SafeLua](http://luaos.net/docs/safelua-api.html) | 2011 -- | Lua (SafeLua) | Bare Machine, Native OS, Sandbox |  Linux || 
| [Lively Kernel](http://www.svgopen.org/2008/papers/93-The_Lively_Kernel_Web_Application_Framework/), also [here](http://www.lively-kernel.org/)  | 2008 -- | Javascript | Sandbox | Web browser ||
| [Python-on-a-Chip, PyMite VM](http://code.google.com/p/python-on-a-chip/)  | 2000 -- | Python | Bare machine | PIC, ARM, Arduino, ...<b>microcontrollers | Embedded controllers |
| [Sugar](http://www.ibm.com/developerworks/linux/tutorials/l-sugarpy/), also [here](http://wiki.laptop.org/go/Sugar_Architecture) and [here](http://wiki.laptop.org/go/Understanding_Sugar_code) | 2007 -- | Python | Native OS | OLPC laptop<br>Linux + Gtk | Education |
| [Cleese](https://github.com/jtauber/cleese/) | 2003 --| Python | Bare machine |||
| [Pycorn](http://www.pycorn.org/home) | 2008 -- | Python | Bare machine | Gumstix Verdex board<br>(ARM processor) | Education |
| [Python OS Project (POP)](http://python-os.info/en/) | 2009 -- | Python | Native OS | Linux | Desktop OS<br>"Just For Fun" |
| [OSDev.org](http://wiki.osdev.org/), also [here](http://wiki.osdev.org/Projects) | 2008 -- | various | various | various | various |

Key to **Substrate** column

* **Bare machine** 
The system includes an operating system kernel written mostly
in the favored language, with only a minimal amount of C or assembler.
The "bare machine" might actually be virtual machine or emulator
such as QEMU.

* **Virtual Machine** Similar to Bare Machine, but the system is designed from the
beginning to be deployed only on VMs.

* **Native OS** The system runs on top of a conventional OS, whose facilities are
all available.  Programmers and users can avoid utilities not written in the favored language.

* **Sandbox** The system runs on top of a conventional OS, but in a self-contained
environment where most of the the host's facilities are not available.
Programmers and users can only use the utilities provided in the
favored language.

* **OS components** The system runs on a minimal OS built from components chosen from a
collection such as [Flux OSKit](http://www.cs.utah.edu/flux/oskit/).
A more recent collection is
[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html).

[OSDev.org](http://wiki.osdev.org/) has many pages on creating and
experimenting with operating systems.
