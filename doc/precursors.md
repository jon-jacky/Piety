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

> "... *in programming there is a widespread first order theory that one
> shouldn't build one's own tools, languages, and especially operating
> systems.  This is true --- an incredible amount of time and energy has
> gone down these ratholes.  On the second hand, if you* **can** *build your
> own tools, languages, and operating systems you* **absolutely should**
> *because the leverage that can be obtained (and often the time not
> wasted in trying to fix other people's not quite right tools) can be
> incredible.*"

Here are some examples.

| System | Era | Language | Substrate    | Platform  | Applications, Goals |
| ------ | --- | -------- | -------- | -------   | ------- |
| [MCP](http://en.wikipedia.org/wiki/MCP_%28Burroughs_Large_Systems%29), also [here](http://en.wikipedia.org/wiki/Burroughs_large_systems) and [here](http://ed-thelen.org/comp-hist/B5000-AlgolRWaychoff.html) and [here](http://retro-b5500.blogspot.com/2012/03/starting-project.html) ([via](http://www.metafilter.com/122701/STORIES-ABOUT-THE-B5000-AND-PEOPLE-WHO-WERE-THERE-By-Richard-Waychoff)), don't miss [this](http://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-2-pdf/k-2-c1039-ALGOL-B205.pdf) and [this](http://www.cs.virginia.edu/brochure/images/manuals/b5000/brochure/b5000_broch.html) | 1961-- | Algol (ESPOL) | Bare machine | Burroughs B5000 | Data processing, "simpler, faster, less costly programming ... completely automatic operation ... a computer system that's *easier to use!*" |
| [Unix](http://cm.bell-labs.com/cm/cs/who/dmr/hist.html), also [here](http://genius.cat-v.org/ken-thompson/interviews/unix-and-beyond)  | 1969 -- | C | Bare machine | PDP 7, PDP 11, ... | Programming, Document preparation, "not just a good environment in which to do programming, but a system around which a fellowship could form"  |
| [FORTH](http://www.forth.com/resources/evolution/index.html), also [here](http://dl.acm.org/citation.cfm?id=805586) | 1970 -- | FORTH | Bare machine | various minicomputers, microprocessors | Embedded control, "replacing the entire 'vast hierarchy' with a single layer", "extremely efficient use of core and time" |
 [Smalltalk](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls78.html), also [here](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls81.html) and [here](http://propella.sakura.ne.jp/earlyHistoryST/EarlyHistoryST.html) and [here](http://www.vpri.org/pdf/m2004001_power.pdf) and [here](http://news.ycombinator.com/item?id=4229788) | 1970s | Smalltalk | Bare machine | Xerox Alto, Dorado, ... (purpose-built) | "support children of all ages in the world of information", "a language powerful enough to write its own OS but in the friendly form of ... a scripting language" |
| [Lisp Machines](http://en.wikipedia.org/wiki/Lisp_machine), also [here](http://www.ugcs.caltech.edu/~weel/lispm.php) and [here](http://www.andromeda.com/people/ddyer/lisp/) and [here](http://www.ugcs.caltech.edu/~weel/lispm/genera-concepts.pdf) and [here](http://dspace.mit.edu/handle/1721.1/5751) and [here](http://www.sts.tu-harburg.de/~r.f.moeller/symbolics-info/development-environment/index.html) | 1970s, 80s | Lisp | Bare machine | MIT CONS, Symbolics, LMI, ... (purpose-built) | "The Lisp machine is a personal computer ... each person gets his own. ... likely to cost about $80,000 ... (for one user at a time)" |
| [Oberon](http://en.wikipedia.org/wiki/Oberon_%28operating_system%29), also [here](http://www.ethoberon.ethz.ch/) and [here](http://www.ethoberon.ethz.ch/WirthPubl/ProjectOberon.pdf) and [here](http://ignorethecode.net/blog/2009/04/22/oberon/) and [here](http://www.ethoberon.ethz.ch/SYSTEM.html) and [here](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.31.4534) and [here](http://news.ycombinator.com/item?id=593995) | late 1980s | Oberon | Bare machine | ETH Ceres, ... (NS32032 processor) | Programming, Electronics CAD, "an entire system from scratch, ... that can be ... understood as a whole" |
| [Plan 9](http://plan9.bell-labs.com/sys/doc/9.html), also [here](http://doc.cat-v.org/plan_9/) and [here](http://bendyworks.com/geekville/lab_projects/2012/11/getting-plan-9-running-on-the-raspberry-pi) | late 1980s -- | C, Alef | Bare machine | various | Programming, Electronics CAD, "a user builds a private computing environment and recreates it wherever desired" |
| [RISC OS](https://www.riscosopen.org/content/), also [here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=55&t=22093) and [here](http://news.ycombinator.com/item?id=4752949) | 1987 -- | BASIC | Bare machine | Acorn Archimedes, RiscPC, Raspberry Pi, various (ARM processors) | "an insta-booting machine with BASIC", "(that) scales up very well to large applications and even down to system programming" |
|  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/) | 1997 -- | C | Bare machine | x86, StrongArm, various | OS components, "to lower the barrier to entry to OS R&D and to lower its costs" |
| ["Scheme Machine"](http://lists.tunes.org/archives/lispos/1998-December/002514.html) | 1998 | Scheme (MzScheme) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | "For now, it's just fun" |
| [ML/OS](http://dspace.mit.edu/bitstream/handle/1721.1/47545/40495469.pdf), also [here](http://www.cs.utah.edu/flux/papers/oskit-sosp97.html) | 1997 | ML (SML/NJ) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | "demonstrate ... advanced ... features such as continuations and type safety in system-level programming" |
| [Squeak](http://www.squeak.org/), also [here](http://ftp.squeak.org/docs/OOPSLA.Squeak.html) | 1997 -- | Smalltalk | Sandbox | various | "development environment in which to build educational software"  |
| [SqueakNOS](http://squeaknos.blogspot.com/), also [here](http://sourceforge.net/projects/squeaknos/) and [here](http://wiki.squeak.org/squeak/1762) and [here](http://wiki.squeak.org/squeak/5727) | 2006 -- | Smalltalk | Bare machine | x86, various | "Squeak No Operating System", "We want to get rid of the operating system under Squeak" |
| [JavaOS](http://en.wikipedia.org/wiki/JavaOS), also [here](http://www.amazon.com/Inside-JavaOS-TM-Operating-System/dp/0201183935)| 1996 -- 1999 | Java | Bare machine | Sun JavaStation (microSPARC) network computer | "distributed processing, not server-centric processing ... a *client* operating system" |
|[JX](http://www4.cs.fau.de/Projects/JX/) | 1999 -- | Java | Bare machine | x86, "Many ... components, for example the file system, also run on an unmodified JVM" | "benefit from the modern software technology of this object-oriented type-safe language" |
| [JNode](http://www.jnode.org/) | 2003 -- | Java | Bare machine | x86 | "Any Java application should run on it, fast and secure!" |
| [A2, BlueBottle, AOS](http://www.oberon.ethz.ch/), also [here](http://www.ocp.inf.ethz.ch/wiki/Documentation/Front) and [here](http://bluebottle.ethz.ch/) and [here](http://bbos.org/xref/) | 2003 -- | Oberon | Bare machine | x86, ARM | "a single-user, multi-core, multi-tasking system that runs on bare hardware or on top of a host operating system." |
| [hOp, House](http://programatica.cs.pdx.edu/House/) | 2004 -- | Haskell | Bare machine | x86 | "more secure and more reliable software systems" | 
| [HaLVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), also [here](https://github.com/GaloisInc/HaLVM), and [HaNS](http://www.haskell.org/pipermail/haskell-cafe/2011-May/092291.html) | 2010 -- | Haskell | Virtual Machine | Xen hypervisor | "experimental network services" |
| [Mirage](http://www.openmirage.org/), also [here](http://www.openmirage.org/wiki/papers) and [here](http://dl.acm.org/citation.cfm?id=1863114)| 2006 -- | O'Caml | Virtual Machine | Xen hypervisor | "I/O intensive cloud services ... minimize the use and cost of cloud resources" |
| [STEPS]( http://vpri.org/html/work/ifnct.htm), also [here](http://www.vpri.org/pdf/tr2011004_steps11.pdf) and [here](http://news.ycombinator.com/item?id=3996209) | 2006 -- |  [OMeta](http://tinlizzie.org/ometa/), [Nile](http://www.vpri.org/vp_wiki/index.php/Gezira), [Maru](http://piumarta.com/software/maru/), Nothing, ... "Problem-oriented languages" | Bare machine |  various | "recreating (personal computing) ... in less than 1/1000 the amount of program code" | 
| [movitz](http://common-lisp.net/project/movitz/) | 2004 -- | Lisp (CL) |  Bare machine | x86 | "development platform for operating system kernels, embedded, and single-purpose applications" |
| [Gracle](http://dept-info.labri.fr/~strandh/gracle.ps), also [here](gracle_excerpts.txt) | 2004 -- | Lisp (CL) | Native OS | Linux | "single-level store ... objects in main memory are all persistent" | 
| [LOSAK](http://losak.sourceforge.net/) | 2004 -- | Lisp (LOSAK) | Bare machine | QEMU, Bochs | "OS kernel ... implemented with a partial evaluator ... pre-emptive multitasking, ... real-time garbage collection"|
| [Armpit Scheme](http://armpit.sourceforge.net/), other embedded Schemes | 2006 -- | Scheme | Bare machine | ARM (BeagleBoard XM, etc.) | "'Scheme to the metal' ... running without any other OS. ... turning the MCU into a rudimentary Scheme machine. " |
| [LispmFPGA](http://www.aviduratas.de/lisp/lispmfpga/), also [here](https://groups.google.com/forum/?fromgroups=#!topic/comp.lang.lisp/36_qKNErHAg) | 2006 -- | Lisp (CL subset) | Bare machine (FPGA) | Spartan 3 Xilinx FPGA, Digilent Spartan 3 Starter Kit | "a CPU with Lisp optimized instruction set together with a complete set of system software written in Lisp" |
| [IGOR](http://opencores.org/project,igor), also [here](http://www.idi.ntnu.no/news/index.php?news=163) and [here](http://www.flickr.com/photos/kaitorge/sets/72157609445719327/show/) | 2008 -- 2010 | Lisp | Bare machine (FPGA) | Custom PCB with FPGA | "Fourteen students have collaborated in constructing a Lisp machine (IGOR) from scratch."|
| [DreamOS](http://www.stripedgazelle.org/joey/dreamos.html), also [here](http://www.stripedgazelle.org/joey/dream.html) and [here](https://groups.google.com/forum/?fromgroups=#!topic/comp.lang.scheme/qwhCVbPZQvk) | 2009 | Scheme (R4RS) | Bare machine | X86 (Bochs) | "compiled using an x86 assembler written in Scheme" |
| [lisPImachine](http://lispm.dyndns.org/), also [here](http://lispm.dyndns.org/ccl) | 2012 | Lisp (Clozure CL) | Native OS | Linux (Raspian) on Raspberry Pi | "Linux on the command line, ... the SLIME development environment for Common Lisp based on Emacs and ... Clozure Common Lisp" |
| [Boot-to-Guile](https://lists.gnu.org/archive/html/guile-user/2013-02/msg00131.html), also [here](http://savannah.gnu.org/forum/forum.php?forum_id=7506) | 2013 | Scheme (Guile) | Native OS | Linux (QEMU image) | "a familiar & friendly REPL, run straight from the initrd!" |
| [Singularity](http://research.microsoft.com/en-us/projects/singularity/) | 2004 -- | C# | Bare machine | x86 | "more reliable systems and applications" | 
| [Cosmos](http://cosmos.codeplex.com/) | 2007 -- | C# | Bare machine | x86 | OS components, "complete construction kit built from the ground up in C#" |
| [JONESFORTH](http://rwmj.wordpress.com/2010/08/07/jonesforth-git-repository/), also [here](http://git.annexia.org/?p=jonesforth.git;a=summary) and [here](https://github.com/nornagon/jonesforth) and [here](https://raw.github.com/nornagon/jonesforth/master/jonesforth.S) and [here](https://raw.github.com/nornagon/jonesforth/master/jonesforth.f) | 2007 -- | FORTH | Native OS | Linux | " a FORTH program in 2,000 lines ... which will boot and provide an entire development environment (inc. editor, compiler etc)" |
| [Khoros](http://outofhanwell.wordpress.com/2008/08/16/khoros-a-lua-operating-system/), [lv0](http://lv0.org/), also [here](http://lua-users.org/lists/lua-l/2011-08/msg01189.html) | 2008 -- | Lua, C | Bare machine | x86-64 | "elite, micro, minimal, nano, old school, pico, retro, rock solid, secure, simple, stable, straight edge or suckless OS" |
| [eLua](http://www.eluaproject.net/doc/v0.8/en_arch_overview.html) | 2011? -- | Lua, C | Bare machine | [eLuaBrain](http://eluabrain.blogspot.fr/) (Cortex-M3) and many more | "embedded software ... with the power of Lua ... on a wide range of microcontroller architectures" |
| [LuaOs](http://luaos.net/docs/manual.php), [SafeLua](http://luaos.net/docs/safelua-api.html) | 2011 -- | Lua (SafeLua) | Bare machine, Native OS, Sandbox |  Linux | "customizable light-weight sandboxes ... run untrusted code safely" | 
| [ES Operating System](http://code.google.com/p/es-operating-system/), also [here](http://code.google.com/p/es-operating-system/wiki/XV_Semana_Informatica) | 2004 -- | Javascript ("ECMAScript"), C++ | Bare machine | x86 | "pure component operating system ... components written in C++ can be seamlessly controlled from ECMAScript" |
| [Lively Kernel](http://www.svgopen.org/2008/papers/93-The_Lively_Kernel_Web_Application_Framework/), also [here](http://www.lively-kernel.org/)  | 2008 -- | Javascript | Sandbox | Web browser | "An IDE ... self-supporting ... inside the browser without any external tools" |
| [OS.js](http://andersevenrud.github.com/OS.js/) | 2012 -- | Javascript | Sandbox | WebKit and Gecko based browsers | "Cloud/Web Desktop platform" | 
|[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html) | 2009 -- | C | Bare machine | x86 | OS components, used in Stanford [CS140](http://www.scs.stanford.edu/12au-cs140/) course |
| [Erlang on Xen](http://erlangonxen.org/) | 2011 -- | Erlang | Virtual machine | Xen hypervisor | "running Erlang on the bare virtual iron ... startup latency 100-1000 times lower than ... typical Linux + Erlang" |
| [Python-on-a-Chip, PyMite VM](http://code.google.com/p/python-on-a-chip/), also [here](http://wiki.python.org/moin/PyMite)  | 2000 -- | Python | Bare machine | PIC, ARM, Arduino, ... | "runs a significant subset of the Python language on microcontrollers without an OS" |
| [Cleese](https://github.com/jtauber/cleese/), also [here](http://code.google.com/p/cleese/) | 2003, 2009 | Python | Bare machine | x86 | "microkernel mostly based on the Python VM and all other OS functionality written in Python" |
| [Unununium](http://mail.python.org/pipermail/python-announce-list/2004-July/003220.html), also [here](http://web.archive.org/web/20061013010205/http://www.unununium.org/) | 2004 -- 2006 | Python | OS components, then Native OS |  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), then Linux | "create a better computing environment by maximizing interconnection between components" |
| [Sugar](http://www.ibm.com/developerworks/linux/tutorials/l-sugarpy/), also [here](http://wiki.laptop.org/go/Sugar_Architecture) and [here](http://wiki.laptop.org/go/Understanding_Sugar_code) and [here](http://www.sugarlabs.org/index.php) | 2007 -- | Python | Native OS | OLPC laptop, Linux + Gtk | "an inexpensive laptop project intended to help educate children around the world" |
| [Pycorn](http://www.pycorn.org/home), also [here](https://github.com/tornewuff/pycorn) | 2008 -- | Python | Bare machine | Gumstix Verdex board (ARM processor) | "interpreter-centric OS ... access to the full capabilities of the computer ... educational ... fun!" |
| [Python OS Project (POP)](http://python-os.info/en/) | 2009 -- | Python | Native OS | Linux | "Fun ... easy to modify OS" "Dominate desktop OS market!" |
| [raspi+python+ipython](http://www.pythononwheels.org/post/blog) | 2013 | Python | Native OS | Linux (Raspian) on Raspberry Pi | "using [IPython as a shell](http://transneptune.net/2009/06/16/ipython-as-your-default-shell/) ... works on any Linux" |

Key to **Substrate** column

* **Bare machine** 
The system includes an operating system kernel written mostly
in the favored language, with only a minimal amount of C or assembler.
The "bare machine" might actually be virtual machine or emulator
such as QEMU or Bochs.

* **Virtual Machine** Similar to Bare machine, but the system is
designed from the beginning to be deployed only on VMs.

* **OS components** The system runs on a minimal OS built from
components chosen from a collection such as [Flux OSKit](http://www.cs.utah.edu/flux/oskit/),
[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html),
or [Cosmos](http://cosmos.codeplex.com/).

* **Native OS** The system runs on top of a conventional OS.
Programmers and users working in the favored language can mostly avoid
the conventional OS.

* **Sandbox** The system runs on top of a conventional OS, in a
self-contained environment where most of the the host's facilities are
not available.  Programmers and users working in the sandbox can only
use the utilities provided in the favored language.

Not shown in the table are several OS for mobile devices: 
[Chromium](http://dev.chromium.org/chromium-os)
(also [here](http://dev.chromium.org/chromium-os/chromiumos-design-docs/software-architecture)),
[Android](http://www.android-x86.org/) 
(also [here](http://www.tbray.org/ongoing/When/201x/2010/11/14/What-Android-Is)), 
[Firefox OS](http://en.wikipedia.org/wiki/Firefox_OS) 
(aka [B2G](https://wiki.mozilla.org/B2G/Architecture)),
[Joli OS](http://en.wikipedia.org/wiki/Joli_OS),
and [iOS](http://developer.apple.com/library/ios/#documentation/Miscellaneous/Conceptual/iPhoneOSTechOverview/Introduction/Introduction.html).
Each is a Linux (or OS X) kernel supporting a
browser or browser-like applications.  None features a start-from-scratch 
ethos, a single language, or a deliberately simple design.

Many sites provide instructions and examples for building operating
systems: 
[CS140](http://www.scs.stanford.edu/12au-cs140/) (Stanford),
[Baking Pi](http://www.cl.cam.ac.uk/freshers/raspberrypi/tutorials/os/)
(Cambridge), 
[these](http://news.ycombinator.com/item?id=4834008)
(CMU, UMD, MIT, Stanford, Harvard),
[bkerndev](http://www.osdever.net/bkerndev/index.php),
[JamesM](http://www.jamesmolloy.co.uk/tutorial_html/),
[OSDev.org](http://wiki.osdev.org/), ...

Here are more links on operating system 
[design](http://jon-jacky.github.com/home/links.html#design-examples)
and [history](http://jon-jacky.github.com/home/links.html#history).

