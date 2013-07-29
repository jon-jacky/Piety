Here are some examples of system software and utilities written in
Python, or programmable in Python.

| Component | Type | Python role | Description |
| --------- | ---- | ----------- | ----------- |
| [Python Standard Library](http://docs.python.org/2/library/) | Library | Source, binding, API | Source code in [Python](http://hg.python.org/cpython/file/tip/Lib) and [C](http://hg.python.org/cpython/file/tip/Modules) |
| [Other popular libraries](http://wiki.python.org/moin/UsefulModules) | Libraries | Source, binding, API | From the [Python Wiki](http://wiki.python.org/moin/). Includes many alternatives not shown in this table.  |
| [Applications](http://wiki.python.org/moin/Applications) | Various | Source, etc. | From the [Python Wiki](http://wiki.python.org/moin/). Includes many alternatives not shown in this table. |
| [Editors, IDEs, and shells](http://wiki.python.org/moin/PythonEditors) | Editors, IDEs, shells | Source, etc. | From the [Python Wiki](http://wiki.python.org/moin/). Includes many alternatives not shown in this table. |
| [IPython](http://ipython.org/ipython-doc/dev/index.html) | Shell | Source, API | You can even make IPython your [default system shell](http://transneptune.net/2009/06/16/ipython-as-your-default-shell/) (also [here](http://stackoverflow.com/questions/9844965/how-to-use-ipythons-system-shell-profile-as-your-default-shell-windows-7-64-bi)).  You can [embed the IPython shell](http://stackoverflow.com/questions/5466342/embedded-interactive-shell-in-ipython)  in a Python program (updated [here](https://github.com/ipython/ipython/wiki/Cookbook%3a-Updating-code-for-use-with-IPython-0.11-and-later)). | 
| [FUSE](http://fuse.sourceforge.net/), also [here](http://en.wikipedia.org/wiki/Filesystem_in_Userspace) and [here](https://github.com/terencehonles/fusepy) and [here](http://sourceforge.net/apps/mediawiki/fuse/index.php?title=SimpleFilesystemHowto) | File system | Wrapper, API | "With FUSE it is possible to implement a fully functional filesystem in a userspace program." "a secure method for non privileged users to create and mount their own filesystem implementations." | 
| [muXTCP](https://github.com/enki/muXTCP) | Network | Source, API | "Python userspace TCP/IP Stack" (2005, unmaintained) |
| [TCPStack](https://github.com/dound/vns/blob/master/TCPStack.py), [HTTPServer](https://github.com/dound/vns/blob/master/HTTPServer.py) | Network | Source, API | Lightweight TCP stack and an HTTP server that uses it.  Part of [VNS](http://yuba.stanford.edu/vns/), the "Virtual Network System for teaching and experimentation" (also [here](http://yuba.stanford.edu/vns/files/pub/vns_sigcse.pdf) and [here](http://stackoverflow.com/questions/1581087/python-tcp-stack-implementation#comment2171604_1581087)). |
| [Pcapy](http://oss.coresecurity.com/projects/pcapy.html) | Network | Wrapper, API | "Pcapy is a Python extension module that interfaces with the [libpcap](http://www.tcpdump.org/) packet capture library. Pcapy enables python scripts to capture packets on the network."  Used by VNS [HTTPServer](https://github.com/dound/vns/blob/master/HTTPServer.py) (above). | 
| [Scapy](http://www.secdev.org/projects/scapy/), also [here](http://www.secdev.org/projects/scapy/doc/) and [here](http://www.secdev.org/projects/scapy/doc/usage.html#simple-one-liners) | Network | Wrapper, API | "Scapy is a powerful interactive packet manipulation program. It is able to forge or decode packets of a wide number of protocols, send them on the wire, capture them, match requests and replies, and much more." Uses [libpcap, libdnet, and their Python wrappers](http://www.secdev.org/projects/scapy/portability.html).  |
| [paramiko](http://www.lag.net/paramiko/), also [here](https://github.com/paramiko/paramiko) and [here](http://docs.paramiko.org/) | Network | Source, API | "paramiko is a module for python 2.2 (or higher) that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines." "It is written entirely in python (no C or platform-dependent code) ..." |
| [ws30](https://github.com/jon-jacky/uw_python/blob/gh-pages/winter_2012/week05/ws30.py) | Web server | Source | "ws30 -- the thirty minute web server ... how fast could I write a simple web server in python?"  Simpler than the [server in the standard library](http://docs.python.org/2/library/basehttpserver.html) |
| [Grail](http://en.wikipedia.org/wiki/Grail_%28web_browser%29), also [here](https://github.com/mdoege/grailbrowser) and [here](http://grail.sourceforge.net/info/papers/restofus.html) | Web browser | Source, applets | A web browser in Python written in 1995 by Guido van Rossum.  Abandoned 1999. Supports HTML 2.0.  Requires Tcl/Tk. Works in Python 2.7. [Trail](https://github.com/mdoege/Trail) is a recently enhanced version. |
| [uzbl](http://uzbl.org/), also [here](https://github.com/Dieterbe/uzbl) | Web browser | Wrapper, configuration, client | "Uses WebKitGtk+ for rendering and network interaction", "Uses a set of scripts (mostly Python) ... so things work out of the box; yet plenty of room for customization."  |
| [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) | Graphics | Source, API | "Drawing to the Linux Framebuffer in Python" Writes to /dev/fb0 using fcntl, mmap, struct.  Looks like a general technique for doing low-level I/O in Linux.  Based on C code [here](http://doc.qt.digia.com/3.0/emb-framebuffer-howto.html), but simpler. |
| [Python X Library](http://python-xlib.sourceforge.net/) | Graphics | Source, API | "a fully functional X client library for Python programs. It is written entirely in Python, in contrast to earlier X libraries for Python (the ancient X extension and the newer plxlib) which were interfaces to the C Xlib." |
| [PyCairo](http://www.tortall.net/mu/wiki/CairoTutorial), also [here](http://cairographics.org/pycairo/) | Graphics | Binding | "Cairo is a 2D (vector) graphics library ... (that) provides operations similar to the drawing operators of PostScript and PDF. Operations in cairo including stroking and filling cubic Bézier splines, transforming and compositing translucent images, and antialiased text rendering. All drawing operations can be transformed by any affine transformation (scale, rotation, shear, etc.)", "Cairo is implemented as a library written in the C programming language, but bindings are available for several different programming languages." "Pycairo is a set of Python bindings ..." Cairo can write to the [Linux framebuffer](http://lists.cairographics.org/archives/cairo/2010-July/020378.html). |
| [terminal](http://blog.daum.net/nskystars/2644517) | Terminal | Source | "A Simple Linux Framebuffer Terminal in Python (and C)" using the  [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) discussed above | 
| [tinywm](http://incise.org/tinywm.html) | Window manager | Source | "a tiny window manager that I created as an exercise in minimalism. ... It is only around 50 lines of C. There is also a Python version using python-xlib." |
| [Qtile](http://www.qtile.org/), also [here](http://docs.qtile.org/en/latest/) and [here](https://github.com/qtile/qtile) | Window manager | Source, configuration, API, client | "Qtile is a full-featured, hackable tiling window manager written in Python." |
| [peppy](http://peppy.flipturn.org/), also [here](http://code.google.com/p/peppy/) | Editor | Wrapper, plugins | "an XEmacs-like editor in Python", "an extensible framework in Python that can support editing and viewing many different types of files, not just text files", "wrap(s) the wonderful [Scintilla](http://www.scintilla.org/) editing component", "peppy is extended by plugins. Plugins are based on the [yapsy](http://yapsy.sourceforge.net/) component architecture. |
| [Wily](http://www.cse.yorku.ca/~oz/wily/pythonpaper.html), also [here](http://www.cse.yorku.ca/~oz/wily/python.html) | Editor | Client | "Wily emulates in the Unix and X Windows environment the Acme editor from Plan 9." " Wily is an editing environment which can be extended with Python programs. Instead of using an embedded Python interpreter, Wily talks a simple message protocol, and a module lets Python speak the same protocol." |
| [pip](https://pypi.python.org/pypi/pip), also [here](http://www.pip-installer.org/en/latest/) | Package manager | Source | "A tool for installing and managing Python packages".  Can handle dependencies.  Has a sort of [unofficial API](https://groups.google.com/forum/#!topic/python-virtualenv/_VmM-R1Y8pg). | 
| [Mercurial](http://mercurial.selenic.com/) | Distributed version control | Source, API | Used by the [Python developers](http://www.python.org/dev/peps/pep-0374/).  Here is book chapter about the [architecture](http://www.aosabook.org/en/mercurial.html). |
| [Dulwich](http://www.samba.org/~jelmer/dulwich/docs/) | Distributed version control | Source, API | "a pure-Python implementation of the Git file formats and protocols" |
| [gittle](https://github.com/FriendCode/gittle) | Distributed version control | Source, API | "Pythonic Git for Humans.  Gittle is a high-level pure-python git library. It builds upon dulwich which provides most of the low-level machinery." |
| [buzhug](http://buzhug.sourceforge.net/) | Database | Source, query language | "a pure-Python database engine, using a Pythonic, no-SQL syntax ... The database is implemented as a Python iterator, yielding objects whose attributes are the fields defined when the base is created ; therefore, requests can be expressed as list comprehensions or generator expressions, instead of SQL queries |
| [CodernityDB](http://labs.codernity.com/codernitydb/) | Database | Source, query language | "CodernityDB is opensource, pure Python (no 3rd party dependency), fast (really fast check Speed if you don’t believe in words), multiplatform, schema-less, NoSQL database." |
| [coroutines](http://www.dabeaz.com/coroutines/) | Programming technique | Source | "...  a practical exploration of using Python coroutines (extended generators) for solving problems in data processing, event handling, and concurrent programming."  "Part 7: Writing an Operating System" includes lots of code samples. |

Key to **Python role** column

* **Source**
The component is written in Python.

* **API** 
The component provides an Application Programming Interface: Python
classes and functions that can be called from a user's 
Python program to invoke component behavior.

* **Binding** 
The component is a library written in another language,
with a Python API as an alternative to the native API.

* **Wrapper** 
The component is a program whose core is written in another language,
that is invoked by a Python wrapper.

* **Configuration**
The component can be configured by scripts written in Python.

* **Plugin**
The component can load Python code that extends its behavior.

* **Applet** 
The component is a browser that can download and execute
Python code (the "applet") from a host.

* **Query language** 
The component is a database whose query language is provided as a Python API.

* **Client**
The component is a server that communicates using a protocol that has
a Python API.
