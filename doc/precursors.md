This page provides information and links about some unusual operating
systems.  Most are responses to this impulse:

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

| System |  T  | Era | Language | Substrate    | Platform  | Applications, Goals |
| ------ | --- | --- | -------- | ------------ | --------  | ------------------- |
| [Simon](http://en.wikipedia.org/wiki/Simon_%28computer%29), also [here](http://history-computer.com/ModernComputer/Personal/Simon.html) | P | 1950 | five-hole paper tape code | Bare machine | Simon "mechanical brain" (relay computer) | "less space than a grocery-store box", "can be completely understood by one man" |
| [MCP](http://en.wikipedia.org/wiki/MCP_%28Burroughs_Large_Systems%29), also [here](http://en.wikipedia.org/wiki/Burroughs_large_systems) and [here](http://lambda-the-ultimate.org/node/3234) and [here](http://www.scribd.com/doc/61812037/Barton-B5000) and [here](http://ed-thelen.org/comp-hist/B5000-AlgolRWaychoff.html) and [here](http://retro-b5500.blogspot.com/2012/03/starting-project.html) ([via](http://www.metafilter.com/122701/STORIES-ABOUT-THE-B5000-AND-PEOPLE-WHO-WERE-THERE-By-Richard-Waychoff)), don't miss [this](http://archive.computerhistory.org/resources/text/Knuth_Don_X4100/PDF_index/k-2-pdf/k-2-c1039-ALGOL-B205.pdf) and [this](http://www.cs.virginia.edu/brochure/images/manuals/b5000/brochure/b5000_broch.html) and [this](http://www.cs.virginia.edu/brochure/images/manuals/b5000/descrip/descrip.html) | C | 1961-- | Algol (ESPOL) | Bare machine | Burroughs B5000 | "Higher level programming languages, such as ALGOL,should be employed to the practical exclusion of machine language", "a computer system that's *easier to use!*" |
| [LAP6](http://dl.acm.org/citation.cfm?doid=362686.362690), also [here](http://en.wikipedia.org/wiki/LINC) | R | 1963 --  | "machine language" | Bare machine | LINC, Laboratory INstrument Computer, 2048 12-bit words | "runs efficiently in a 'conversational mode'", "features which may seem highly desirable ... can be so much excess baggage" |
| [ITS](http://en.wikipedia.org/wiki/Incompatible_Timesharing_System), also [here](http://web.mit.edu/6.933/www/Fall2001/AILab.pdf) and [here](http://fare.tunes.org/tmp/emergent/pclsr.htm) (also <a href="ftp://publications.ai.mit.edu/ai-publications/pdf/AIM-161A.pdf">here</a> and [here](ftp://publications.ai.mit.edu/ai-publications/pdf/AIM-238.pdf) and [here](ftp://ftp.cs.indiana.edu/pub/techreports/TR173.pdf), ftp links, view Raw for URLs) | A | 1968 -- 1990 | macro assembler | Bare machine | PDP-6, PDP-10 | "designed for the (MIT) Artificial Intelligence Laboratory ... and tailored to its special requirements" | 
| [OS6](http://www.informatik.uni-trier.de/~ley/pers/hd/s/Strachey:C=.html), also [here](http://comjnl.oxfordjournals.org/content/15/2/117.full.pdf) and [here](http://comjnl.oxfordjournals.org/content/15/3/195.full.pdf) | A | 1969 -- | BCPL | Bare machine | Modular One minicomputer | "write the entire system in one high-level language" "... (compiled to instructions for an) interpreter (that) behaves as a virtual machine" | 
| [Unix](http://cm.bell-labs.com/cm/cs/who/dmr/hist.html), also [here](http://genius.cat-v.org/ken-thompson/interviews/unix-and-beyond)  | C | 1969 -- | C | Bare machine | PDP 7, PDP 11, ... | Programming, Document preparation, "not just a good environment in which to do programming, but a system around which a fellowship could form"  |
| [FORTH](http://www.forth.com/resources/evolution/index.html), also [here](http://dl.acm.org/citation.cfm?id=805586) | C | 1970 -- | FORTH | Bare machine | various minicomputers, microprocessors | Embedded control, "replacing the entire 'vast hierarchy' with a single layer", "extremely efficient use of core and time" |
| [Alto OS](http://research.microsoft.com/apps/pubs/default.aspx?id=68223), also [here](http://research.microsoft.com/en-us/um/people/blampson/38-AltoSoftware/WebPage.html) and [here](research.microsoft.com/en-us/um/people/blampson/38-AltoSoftware/ThackerAltoHardware.pdf) and [here](http://xeroxalto.computerhistory.org/xerox_alto_file_system_archive.html) | R | 1973 -- | BCPL | Bare machine | Xerox Alto (purpose built) | "open design, which allows any part of the system to be replaced by a client program" |
| [Smalltalk](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls78.html), also [here](http://classes.soe.ucsc.edu/cmps112/Spring03/readings/Ingalls81.html) and [here](http://propella.sakura.ne.jp/earlyHistoryST/EarlyHistoryST.html) and [here](http://www.vpri.org/pdf/m2004001_power.pdf) and [here](http://news.ycombinator.com/item?id=4229788) | R | 1973 -- | Smalltalk | Bare machine | Xerox Alto, Dorado, ... (purpose-built) | "support children of all ages in the world of information", "a language powerful enough to write its own OS but in the friendly form of ... a scripting language" |
| [Lisp Machines](http://en.wikipedia.org/wiki/Lisp_machine), also [here](http://www.ugcs.caltech.edu/~weel/lispm.php) and [here](http://www.andromeda.com/people/ddyer/lisp/) and [here](http://www.ugcs.caltech.edu/~weel/lispm/genera-concepts.pdf) and [here](http://dspace.mit.edu/handle/1721.1/5751) (pictured [here](http://www.computerhistory.org/chess/full_record.php?iid=stl-431614f64ea3e)) and [here](http://www.sts.tu-harburg.de/~r.f.moeller/symbolics-info/development-environment/index.html) and and [here](http://www.cliki.net/VLM_on_Linux) and [here](http://www.loper-os.org/?p=932) | C | 1970s, 80s | Lisp | Bare machine | MIT CONS, Symbolics, LMI, ... (purpose-built) | "The Lisp machine is a personal computer ... each person gets his own. ... likely to cost about $80,000 ... (for one user at a time)" |
| [iMAX](http://dl.acm.org/citation.cfm?id=806601), also [here](http://dl.acm.org/citation.cfm?id=989818) and [here](https://blogs.oracle.com/bmc/entry/revisiting_the_intel_432) and [here](http://bitsavers.informatik.uni-stuttgart.de/pdf/intel/iAPX_432/172103-002_iMAX_432_Reference_Manual_May82.pdf) | C | 1981 -- 1985 | Ada | Bare machine | Intel iAPX 432 processor | "uniformly structure the hardware and software of the system around a single set of concepts based on objects", "perhaps the largest existing piece of operational software written in Ada" |
| [Oberon](http://en.wikipedia.org/wiki/Oberon_%28operating_system%29), also [here](http://www.ethoberon.ethz.ch/) and [here](http://www.ethoberon.ethz.ch/WirthPubl/ProjectOberon.pdf) and [here](http://ignorethecode.net/blog/2009/04/22/oberon/) and [here](http://www.ethoberon.ethz.ch/SYSTEM.html) and [here](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.31.4534) and [here](http://news.ycombinator.com/item?id=593995) | A | 1985 -- | Oberon | Bare machine | ETH Ceres, ... (NS32032 processor) | Programming, Electronics CAD, "an entire system from scratch, ... that can be ... understood as a whole" |
| [Project Oberon](http://www.inf.ethz.ch/personal/wirth/ProjectOberon/) (New Edition 2013), also [here](http://wirth-symposium.ethz.ch/speakers.html#Wirth) and [here](http://wirth-symposium.ethz.ch/slides/wirth.pdf) | A | 2013 | Oberon | Bare Machine | Custom CPU on FPGA (Xilinx Spartan 3, Digilent board) | "extend the desire for simplicity and regularity to the hardware" |
| [Plan 9](http://plan9.bell-labs.com/sys/doc/9.html), also [here](http://doc.cat-v.org/plan_9/) and [here](http://bendyworks.com/geekville/lab_projects/2012/11/getting-plan-9-running-on-the-raspberry-pi) | R | late 1980s -- | C, Alef | Bare machine | various | Programming, Electronics CAD, "a user builds a private computing environment and recreates it wherever desired" |
| [RISC OS](https://www.riscosopen.org/content/), also [here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=55&t=22093) and [here](http://news.ycombinator.com/item?id=4752949) and [here](https://www.riscosopen.org/content/sales/risc-os-pico) | C | 1987 -- | BASIC | Bare machine | Acorn Archimedes, RiscPC, Raspberry Pi, various (ARM processors) | "an insta-booting machine with BASIC", "(that) scales up very well to large applications and even down to system programming" |
| [RaspberryPi BASIC](http://highcaffeinecontent.com/rpi/), also [here](https://news.ycombinator.com/item?id=8228763) | P | 2014 | C++, BASIC | Bare Machine | Raspberry Pi | "bare-metal operating system that boots directly to a BASIC prompt ... the kernel is written in C++" |
| [Bauhaus](http://lispm.de/lisp-based-newton-os), also [here](https://news.ycombinator.com/item?id=7781265) (especially [this](https://news.ycombinator.com/item?id=7782146)) and [here](https://news.ycombinator.com/item?id=320646) | C | 1992 -- 1994 | "Ralph: Scheme+CLOS variant, later known as Dylan" | Native OS (embedded kernel) | Apple Newton PDA prototype, ARM (not shipped) | "very easy to ... add new features or change functionality" |
|  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/) | A | 1997 -- | C | Bare machine | x86, StrongArm, various | OS components, "to lower the barrier to entry to OS R&D and to lower its costs" |
| ["Scheme Machine"](http://lists.tunes.org/archives/lispos/1998-December/002514.html) | S | 1998 | Scheme (MzScheme) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | "For now, it's just fun" |
| [ML/OS](http://dspace.mit.edu/bitstream/handle/1721.1/47545/40495469.pdf), also [here](http://www.cs.utah.edu/flux/papers/oskit-sosp97.html) | S | 1997 | ML (SML/NJ) | OS components | [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), x86 | "demonstrate ... advanced ... features such as continuations and type safety in system-level programming" |
| [Squeak](http://www.squeak.org/), also [here](http://ftp.squeak.org/docs/OOPSLA.Squeak.html) | R | 1997 -- | Smalltalk | Sandbox | various | "development environment in which to build educational software"  |
| [SqueakNOS](http://squeaknos.blogspot.com/), also [here](http://sourceforge.net/projects/squeaknos/) and [here](http://wiki.squeak.org/squeak/1762) and [here](http://wiki.squeak.org/squeak/5727) | P | 2006 -- | Smalltalk | Bare machine | x86, various | "Squeak No Operating System", "We want to get rid of the operating system under Squeak" |
| [MaRTE OS](http://marte.unican.es/) | A | 2000 -- | Ada | Native OS or Bare machine | Linux, x86 | "runtime for Ada applications ... run as a normal Linux process ... or as binary for an x86 bare machine" | 
| [JavaOS](http://en.wikipedia.org/wiki/JavaOS), also [here](http://www.amazon.com/Inside-JavaOS-TM-Operating-System/dp/0201183935)| C | 1996 -- 1999 | Java | Bare machine | Sun JavaStation (microSPARC) network computer | "distributed processing, not server-centric processing ... a *client* operating system" |
|[JX](http://www4.cs.fau.de/Projects/JX/) | A | 1999 -- | Java | Bare machine | x86, "Many ... components, for example the file system, also run on an unmodified JVM" | "benefit from the modern software technology of this object-oriented type-safe language" |
| [JNode](http://www.jnode.org/) | R | 2003 -- | Java | Bare machine | x86 | "Any Java application should run on it, fast and secure!" |
|[Haiku](https://www.haiku-os.org/), also [here](http://www.osnews.com/story/24945/A_Programmer_s_Introduction_to_the_Haiku_OS) and [here](http://spectrum.ieee.org/computing/software/the-dawn-of-haiku-os/0) | R | 2001 -- | C++ | Bare machine | x86, ARM, PPC | "pervasive multithreading", "in C++ as a series of programmer-accessible objects" |
| [A2, BlueBottle, AOS](http://www.oberon.ethz.ch/), also [here](http://www.ocp.inf.ethz.ch/wiki/Documentation/Front) and [here](http://bluebottle.ethz.ch/) and [here](http://bbos.org/xref/) | A | 2003 -- | Oberon | Bare machine | x86, ARM | "a single-user, multi-core, multi-tasking system that runs on bare hardware or on top of a host operating system." |
| [Contiki](http://www.contiki-os.org/#about), with [lwIP and uIP](http://dunkels.com/adam/software.html) network stacks, also [here](http://dunkels.com/adam/publications-abstracts.html#dunkels04contiki) and [here](http://dunkels.com/adam/publications-abstracts.html#dunkels03full) and [here](http://www.wired.com/2014/06/contiki/) | A | 2003 -- | C | Bare machine | 8-bit microcontrollers: TI MSP430, Amtel AVR | "tiny networked sensors", "dynamically download code", "full TCP/IP for 8-bits" |
| [hOp, House](http://programatica.cs.pdx.edu/House/) | A | 2004 -- | Haskell | Bare machine | x86 | "more secure and more reliable software systems" | 
| [HaLVM](http://corp.galois.com/blog/2010/11/30/galois-releases-the-haskell-lightweight-virtual-machine-halv.html), also [here](https://github.com/GaloisInc/HaLVM), and [HaNS](http://www.haskell.org/pipermail/haskell-cafe/2011-May/092291.html) | R | 2010 -- | Haskell | Virtual Machine | Xen hypervisor | "experimental network services" |
| [Mirage](http://www.openmirage.org/), also [github](https://github.com/mirage) and [papers](http://www.openmirage.org/wiki/papers) and  [Xen](http://www.xenproject.org/developers/teams/mirage-os.html) and [paper](http://cacm.acm.org/magazines/2014/1/170866-unikernels/abstract) and [HN](https://news.ycombinator.com/item?id=8109912) | A | 2006 -- | O'Caml | Virtual Machine | Xen hypervisor | "I/O intensive cloud services ... minimize the use and cost of cloud resources" |
| [STEPS]( http://vpri.org/html/work/ifnct.htm), also [here](http://www.vpri.org/pdf/tr2011004_steps11.pdf) and [here](http://news.ycombinator.com/item?id=3996209) | R | 2006 -- |  [OMeta](http://tinlizzie.org/ometa/), [Nile](http://www.vpri.org/vp_wiki/index.php/Gezira), [Maru](http://piumarta.com/software/maru/), Nothing, ... "Problem-oriented languages" | Bare machine |  various | "recreating (personal computing) ... in less than 1/1000 the amount of program code" | 
| [Schemix](http://www.abstractnonsense.com/schemix/), also [here](https://news.ycombinator.com/item?id=6589165) | P | 2003 | Scheme (TinyScheme) | Native OS | "implemented as a patch to the Linux kernel" | "exploration of the Linux kernel ... rapid, interactive prototyping of Linux drivers and ... kernel features" |
| [movitz](http://common-lisp.net/project/movitz/), also [here](https://news.ycombinator.com/item?id=6589986) | P | 2004 -- | Lisp (CL) |  Bare machine | x86 | "development platform for operating system kernels, embedded, and single-purpose applications" |
| [Gracle](http://dept-info.labri.fr/~strandh/gracle.ps), then [LispOs](https://github.com/robert-strandh/LispOS), also [here](gracle_excerpts.txt) | P | 2004 -- | Lisp (CL) | Native OS | Linux | "single-level store ... objects in main memory are all persistent" | 
| [LOSAK](http://losak.sourceforge.net/), then [multischeme](https://github.com/ojarjur/multischeme), also [here](https://news.ycombinator.com/item?id=7166755) | P | 2004 -- | Lisp (LOSAK), then Scheme | Bare machine | QEMU, Bochs | "OS kernel ... implemented with a partial evaluator ... pre-emptive multitasking, ... real-time garbage collection"|
| [Armpit Scheme](http://armpit.sourceforge.net/), other embedded Schemes | A | 2006 -- | Scheme | Bare machine | ARM (BeagleBoard XM, etc.) | "'Scheme to the metal' ... running without any other OS. ... turning the MCU into a rudimentary Scheme machine. " |
| [LispmFPGA](http://www.aviduratas.de/lisp/lispmfpga/), also [here](https://groups.google.com/forum/?fromgroups=#!topic/comp.lang.lisp/36_qKNErHAg) | P | 2006 -- | Lisp (CL subset) | Bare machine (FPGA) | Spartan 3 Xilinx FPGA, Digilent Spartan 3 Starter Kit | "a CPU with Lisp optimized instruction set together with a complete set of system software written in Lisp" |
| [IGOR](http://opencores.org/project,igor), also [here](http://www.idi.ntnu.no/news/index.php?news=163) and [here](http://www.flickr.com/photos/kaitorge/sets/72157609445719327/show/) | S | 2008 -- 2010 | Lisp | Bare machine (FPGA) | Custom PCB with FPGA | "Fourteen students have collaborated in constructing a Lisp machine (IGOR) from scratch."|
| [PilMCU](http://www.mail-archive.com/picolisp@software-lab.de/msg04823.html), also [here](http://www.mail-archive.com/picolisp@software-lab.de/msg04837.html) | P | 2014 | [PicoLisp](http://picolisp.com/wiki/?Home) | Bare machine (FPGA) | Verilog simulator only for now | "an implementation of 64-bit PicoLisp directly in hardware. ... PicoLisp is both the machine language and the operating system" |
| [DreamOS](http://www.stripedgazelle.org/joey/dreamos.html), also [here](http://www.stripedgazelle.org/joey/dream.html) and [here](https://groups.google.com/forum/?fromgroups=#!topic/comp.lang.scheme/qwhCVbPZQvk) | P | 2009 | Scheme (R4RS) | Bare machine | X86 (Bochs) | "compiled using an x86 assembler written in Scheme" |
| [lisPImachine](http://lispm.dyndns.org/), also [here](http://lispm.dyndns.org/ccl) | P | 2012 | Lisp (Clozure CL) | Native OS | Linux (Raspian) on Raspberry Pi | "Linux on the command line, ... the SLIME development environment for Common Lisp based on Emacs and ... Clozure Common Lisp" |
| [ECMAchine](http://alex.nisnevich.com/ecmachine/), also [here](https://github.com/AlexNisnevich/ECMAchine) | P | 2012 | Lisp, Javascript | Sandbox | Web browser | "an in-browser Scheme REPL that is also a toy operating system. It has a virtual filesystem ... (and) a rudimentary process management system." |
|[Emacs](http://www.informatimago.com/linux/emacs-on-user-mode-linux.html), pertinent also [here](http://nic.ferrier.me.uk/blog/2010_10/elnode) and [here](http://www.emacswiki.org/emacs/w3) and [here](http://batsov.com/articles/2012/02/19/package-management-in-emacs-the-good-the-bad-and-the-ugly/) | P | 2012 | Emacs Lisp | Native OS | Linux | "Emacs standing alone on a Linux Kernel", also web server, browser, package management  |
| [Boot-to-Guile](https://lists.gnu.org/archive/html/guile-user/2013-02/msg00131.html), also [here](http://savannah.gnu.org/forum/forum.php?forum_id=7506) | P | 2013 | Scheme (Guile) | Native OS | Linux (QEMU image) | "a familiar & friendly REPL, run straight from the initrd!" |
| [Singularity](http://research.microsoft.com/en-us/projects/singularity/) | R | 2004 -- | C# | Bare machine | x86 | "more reliable systems and applications" | 
| [Cosmos](http://cosmos.codeplex.com/) | R | 2007 -- | C# | Bare machine | x86 | OS components, "complete construction kit built from the ground up in C#" |
| [JONESFORTH](http://rwmj.wordpress.com/2010/08/07/jonesforth-git-repository/), also [here](http://git.annexia.org/?p=jonesforth.git;a=summary) and [here](https://github.com/nornagon/jonesforth) and [here](https://raw.github.com/nornagon/jonesforth/master/jonesforth.S) and [here](https://raw.github.com/nornagon/jonesforth/master/jonesforth.f) | P | 2007 -- | FORTH | Native OS | Linux | " a FORTH program in 2,000 lines ... which will boot and provide an entire development environment (inc. editor, compiler etc)" |
| [Khoros](http://outofhanwell.wordpress.com/2008/08/16/khoros-a-lua-operating-system/), [lv0](http://lv0.org/), also [here](http://lua-users.org/lists/lua-l/2011-08/msg01189.html) | P | 2008 -- | Lua, C | Bare machine | x86-64 | "elite, micro, minimal, nano, old school, pico, retro, rock solid, secure, simple, stable, straight edge or suckless OS" |
| [eLua](http://www.eluaproject.net/doc/v0.8/en_arch_overview.html) | R | 2011? -- | Lua, C | Bare machine | [eLuaBrain](http://eluabrain.blogspot.fr/) (Cortex-M3) and many more | "embedded software ... with the power of Lua ... on a wide range of microcontroller architectures" |
| [LuaOs](http://luaos.net/docs/manual.php), [SafeLua](http://luaos.net/docs/safelua-api.html) | P | 2011 -- | Lua (SafeLua) | Bare machine, Native OS, Sandbox |  Linux | "customizable light-weight sandboxes ... run untrusted code safely" | 
| [luakernel](https://github.com/ers35/luakernel), also at [HN](https://news.ycombinator.com/item?id=8486178) | P | 2014 | Lua | Bare machine | x86 | "Lua + SQLite running on bare metal x86" "file primitive ... purely in Lua ... a pre-initialized ramfs" "lua coroutines as the core of the scheduling" |
| [ES Operating System](http://code.google.com/p/es-operating-system/), also [here](http://code.google.com/p/es-operating-system/wiki/XV_Semana_Informatica) | P | 2004 -- | Javascript ("ECMAScript"), C++ | Bare machine | x86 | "pure component operating system ... components written in C++ can be seamlessly controlled from ECMAScript" |
| [Lively Kernel](http://www.svgopen.org/2008/papers/93-The_Lively_Kernel_Web_Application_Framework/), also [here](http://www.lively-kernel.org/)  | R | 2008 -- | Javascript | Sandbox | Web browser | "An IDE ... self-supporting ... inside the browser without any external tools" |
| [OS.js](http://andersevenrud.github.com/OS.js/) | P | 2012 -- | Javascript | Sandbox | WebKit and Gecko based browsers | "Cloud/Web Desktop platform" | 
| [NodeOS](http://nodeos.github.io/blog/introduction/), also [here](https://github.com/NodeOS/Docker-NodeOS) | P | 2013 | Javascript | Native OS | Linux, Docker, Node.js, NPM | "a Node.js based operating system, built off of the Linux kernel" |
|[TempleOS](http://www.templeos.org/Wb/Accts/TS/Wb2/TempleOS.html), also [here](https://github.com/muflax/templeos) and [here](https://news.ycombinator.com/item?id=7589304) | P | c. 2003 -- | [HolyC](http://www.templeos.org/Wb/Doc/HolyC.html#l1), "more than C, less than C++" | Bare Machine | x86_64 | "for recreational programming ... a modern cross between DOS and a Commodore 64" |
|[Pintos](http://www.stanford.edu/class/cs140/projects/pintos/pintos.html) | A | 2009 -- | C | Bare machine | x86 | OS components, used in Stanford [CS140](http://www.scs.stanford.edu/12au-cs140/) course |
|[Drawbridge](http://research.microsoft.com/en-us/projects/drawbridge/), also [here](http://research.microsoft.com/apps/pubs/default.aspx?id=141071) | R | 2010 -- | C++ (?) (based on Windows 7) | Sandbox ("library OS") | Windows 7 | "1/50th the size of the full desktop OS", "strong security isolation" |
| [Erlang on Xen](http://erlangonxen.org/) | R | 2011 -- | Erlang | Virtual machine | Xen hypervisor | "running Erlang on the bare virtual iron ... startup latency 100-1000 times lower than ... typical Linux + Erlang" |
| [GoFY](http://gofy.cat-v.org/), also [here](http://code.google.com/p/gofy/) and [here](https://github.com/machinaut/gofy) | P | 2011 -- | Go | Bare Machine | "x86-64 only" |  "GoFY is a new revolutionary radical operating system that aims to break all rules" |
| [kOS](http://kparc.com/o.htm) and [here](http://kparc.com/$/), also [article](http://archive.vector.org.uk/art10501320) and [HN](https://news.ycombinator.com/item?id=8475809), also [conference](http://www.jsoftware.com/jwiki/Community/Conference2012#Schedule) and [blog](http://coding-is-like-cooking.info/tag/array-languages/) | R | 2012-- | [k](http://archive.vector.org.uk/art10010830) (like APL, also [here](http://kparc.com/k.txt) and [here](http://www.kparc.com/)), C | Bare machine (?) | "k requires nothing. it uses no libraries and has no dependencies." | "for desktop, cloud, pad and phone, e.g. a replacement for webkit and android" | 
| [zero.rs](https://github.com/pcwalton/zero.rs) | P | 2013 | Rust | Native OS | C stdlib: "The only dependencies are ... malloc, free, abort, memcpy, and memcmp" | "create almost completely freestanding Rust programs" |
| [rustboot](https://github.com/charliesome/rustboot), also [here](http://jvns.ca/blog/categories/kernel/) | P | 2013 | Rust | Bare machine | QEMU | "A tiny 32 bit kernel written in Rust" |
| [OSv](http://osv.io/), also [here](http://mailman.cs.huji.ac.il/pipermail/linux-il/2013-September/010649.html) and [here](https://github.com/cloudius-systems/osv) and [here](https://docs.google.com/presentation/d/11mxUl8PBDQ3C4QyeHBT8BcMPGzqk-C8bV1Fw8xLgwSI/preview#slide=id.p) | R | 2013 | C++ | Virtual Machine | KVM, Xen, Amazon EC2, also VMware planned | "run a single application on a virtual machine", "tiny compared to Linux", "less than one second to boot"  |
| [Urbit](http://www.urbit.org/), also [code](https://github.com/urbit/urbit) and [docs](http://doc.urbit.org/) and [video](http://www.youtube.com/watch?v=6S8JFoT6BEM) and [startup](https://angel.co/tlon) and [blog](http://alexkrupp.typepad.com/sensemaking/2013/12/a-brief-introduction-to-urbit.html) and [HN](https://news.ycombinator.com/item?id=6440884) and [more HN](https://news.ycombinator.com/item?id=5110868) | P | 2013 -- | Nock  "a combinator automaton", Hoon "FP made stupid" | Native OS | Linux, OS X | "not much sign of a connection to ordinary Earth computing" |
| [Rump Kernel](https://github.com/rumpkernel/wiki/wiki) | R | 2009 -- | C | Bare machine, Virtual Machine | "... userspace, the Xen hypervisor, bare metal, ..." | OS components: "componentized, kernel quality drivers ... file systems, POSIX system call handlers, PCI device drivers, a SCSI protocol stack and the TCP/IP stack" |
| [rumpuser-baremetal](http://blog.netbsd.org/tnf/entry/an_internet_ready_os_from), also [GitHub](https://github.com/rumpkernel/rumpuser-baremetal) | R | 2014 | C | OS Components | [Rump Kernel](https://github.com/rumpkernel/wiki/wiki), x86-32 | "run an off-the-shelf httpd ... just bolting a lot of working components together ... some hundreds of lines of code" | 
| [Python-on-a-Chip, PyMite VM](http://code.google.com/p/python-on-a-chip/), also [here](http://wiki.python.org/moin/PyMite)  | P | 2000 -- | Python | Bare machine | PIC, ARM, Arduino, ... | "runs a significant subset of the Python language on microcontrollers without an OS" |
| [Cleese](https://github.com/jtauber/cleese/), also [here](http://code.google.com/p/cleese/) | P | 2003, 2009 | Python | Bare machine | x86 | "microkernel mostly based on the Python VM and all other OS functionality written in Python" |
| [Unununium](http://mail.python.org/pipermail/python-announce-list/2004-July/003220.html), also [here](http://web.archive.org/web/20061013010205/http://www.unununium.org/) | P | 2004 -- 2006 | Python | OS components, then Native OS |  [Flux OSKit](http://www.cs.utah.edu/flux/oskit/), then Linux | "create a better computing environment by maximizing interconnection between components" |
| [Pardus Linux](http://en.pardus-wiki.org/Main_Page), also [here](https://github.com/Pardus-Linux) and [here](http://blogs.kde.org/2009/07/12/interesting-things-i-saw-gcds-pardus-linux) and [here](http://web.archive.org/web/20070329062212/http://www.pardus.org.tr/eng/projects/comar/PythonInPardus.html) and [here](http://web.archive.org/web/20061114003057/http://www.pardus.org.tr/eng/projeler/comar/SpeedingUpLinuxWithPardus.html) | R | 2005 -- | Python | Native OS | Linux | Linux distribution that ["uses Python across many of its core tools ... even a new init framework"](http://onlamp.com/onlamp/2007/05/10/rethinking-the-linux-distribution.html)
| [Sugar](http://www.ibm.com/developerworks/linux/tutorials/l-sugarpy/), also [here](http://wiki.laptop.org/go/Sugar_Architecture) and [here](http://wiki.laptop.org/go/Understanding_Sugar_code) and [here](http://www.sugarlabs.org/index.php) | R | 2007 -- | Python | Native OS | OLPC laptop, Linux + Gtk | "an inexpensive laptop project intended to help educate children around the world" |
| [Pycorn](http://www.pycorn.org/home), also [here](https://github.com/tornewuff/pycorn) | P | 2008 -- | Python | Bare machine | Gumstix Verdex board (ARM processor) | "interpreter-centric OS ... access to the full capabilities of the computer ... educational ... fun!" |
| [Python OS Project (POP)](http://python-os.info/en/) | P | 2009  | Python | Native OS | Linux | "Fun ... easy to modify OS" "Dominate desktop OS market!" |
| [raspi+python+ipython](http://www.pythononwheels.org/post/blog) | P | 2013 | Python | Native OS | Linux (Raspian) on Raspberry Pi | "using [IPython as a shell](http://transneptune.net/2009/06/16/ipython-as-your-default-shell/) ... works on any Linux" |
| [Micro Python](http://micropython.org/), also [github](https://github.com/micropython/micropython) and [wiki](https://github.com/micropython/micropython/wiki) and [differences](https://github.com/micropython/micropython/wiki/Differences) and [library](https://github.com/micropython/micropython-lib) and [kickstarter](http://www.kickstarter.com/projects/214379695/micro-python-python-for-microcontrollers) and [interview](http://hackaday.com/2013/11/27/interview-with-damien-george-creator-of-the-micro-python-project/) and [linux](https://mail.python.org/pipermail/python-list/2014-June/673020.html) and [video](http://www.youtube.com/watch?v=hmGISrwPtyA) and [caveats](https://news.ycombinator.com/item?id=7841983) | P | 2013 -- | Python 3 | Bare machine, native OS  | "32-bit ARM with the Thumb v2 instruction set, such as Cortex M. ... tested on an STM32F405 chip", Linux | "complete rewrite, from scratch, of Python. ...  includes a complete parser, compiler, virtual machine, runtime system, garbage collector and support libraries to run on a microcontroller." |

Key to **T** (project **Type**) column, perhaps an indicator of
project size and longevity:

* **C** ommercial product sold to customers, including ongoing support

* **R** esearch and Development, usually sponsored by industry or
government.  Some of these are almost like commercial products
( **C** above), except the product is not sold, but distributed
by other means.

* **A** cademic research by a group at a university, often supported
in part by grants from government or industry

* **S** tudent project by an individual or small group, for a course
or thesis.  Usually development ends when the student completes the
course or graduates.

* **P** ersonal project by an individual or small group


Key to **Substrate** column:

* **Bare machine** 
The system includes an operating system kernel written mostly
In the favored language, with only a minimal amount of C or assembler.
The "bare machine" might actually be virtual machine or emulator
such as QEMU or Bochs.

* **Virtual Machine** Similar to Bare machine, but the system is
designed from the beginning to be deployed only on VMs.

* **OS components** The system runs on a minimal OS built from
components chosen from a collection such as [Flux OSKit](http://www.cs.utah.edu/flux/oskit/) or [Rump Kernel](https://github.com/rumpkernel/wiki/wiki).

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

The table shows some, but not all, of the recent [cloud operating systems](http://www.linux.com/news/enterprise/cloud-computing/751156-are-cloud-operating-systems-the-next-big-thing-).

Many sites provide instructions and examples for building operating
systems: 
[CS140](http://www.scs.stanford.edu/12au-cs140/) (Stanford),
[6.828](http://pdos.csail.mit.edu/6.828/2012/xv6.html) (MIT),
[CS194-24](http://www.cs.berkeley.edu/~kubitron/courses/cs194-24-S13/index_lectures.html) (Berkeley),
[Baking Pi](http://www.cl.cam.ac.uk/freshers/raspberrypi/tutorials/os/)
(Cambridge), 
[OS from Scratch](http://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf) (Birmingham, more in [HN](https://news.ycombinator.com/item?id=8380822)),
[these](http://news.ycombinator.com/item?id=4834008)
(CMU, UMD, MIT, Stanford, Harvard),
[BrokenThorn](http://www.brokenthorn.com/Resources/OSDevIndex.html),
[bkerndev](http://www.osdever.net/bkerndev/index.php),
[JamesM](http://www.jamesmolloy.co.uk/tutorial_html/),
[OSDev.org](http://wiki.osdev.org/), ...

Here are more links on operating system 
[design](http://jon-jacky.github.com/home/links.html#design-examples)
and [history](http://jon-jacky.github.com/home/links.html#history).

