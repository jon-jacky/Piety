Here are some examples of system software and utilities written in
Python, or programmable in Python.

| Component | Type | Python role | Description |
| --------- | ---- | ----------- | ----------- |
| [Python Standard Library](http://docs.python.org/2/library/) | Library | Source, binding, API | Source code in [Python](http://hg.python.org/cpython/file/tip/Lib) and [C](http://hg.python.org/cpython/file/tip/Modules) |
| [Other popular libraries](http://wiki.python.org/moin/UsefulModules) | Libraries | Source, binding, API | From the [Python Wiki](http://wiki.python.org/moin/) |
| [Applications](http://wiki.python.org/moin/Applications) | Various | Source, etc. | From the [Python Wiki](http://wiki.python.org/moin/) |
| [Editors and Shells](http://wiki.python.org/moin/PythonEditors) | Editors, shells | Source, etc. | From the [Python Wiki](http://wiki.python.org/moin/) |
| [TCPStack](https://github.com/dound/vns/blob/master/TCPStack.py) | Network | Source, API | Lightweight TCP stack.  Part of [VNS](http://yuba.stanford.edu/vns/), the "Virtual Network System for teaching and experimentation" (also [here](http://yuba.stanford.edu/vns/files/pub/vns_sigcse.pdf)). |
| [ws30](https://github.com/jon-jacky/uw_python/blob/gh-pages/winter_2012/week05/ws30.py) | Web server | Source | "ws30 -- the thirty minute web server ... how fast could I write a simple web server in python?"  Simpler than the [server in the standard library](http://docs.python.org/2/library/basehttpserver.html) |
| [uzbl](http://uzbl.org/), also [here](https://github.com/Dieterbe/uzbl) | Web browser | Wrapper, configuration, client | "Uses WebKitGtk+ for rendering and network interaction", "Uses a set of scripts (mostly Python) ... so things work out of the box; yet plenty of room for customization."  |
| [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) | Graphics | Source, API | "Drawing to the Linux Framebuffer in Python" Writes to /dev/fb0 using fcntl, mmap, struct.  Looks like a general technique for doing low-level I/O in Linux.  Based on C code [here](http://doc.qt.digia.com/3.0/emb-framebuffer-howto.html), but simpler. |
| [Python X Library](http://python-xlib.sourceforge.net/) | Graphics | Source, API | "a fully functional X client library for Python programs. It is written entirely in Python, in contrast to earlier X libraries for Python (the ancient X extension and the newer plxlib) which were interfaces to the C Xlib." |
| [PyCairo](http://www.tortall.net/mu/wiki/CairoTutorial), also [here](http://cairographics.org/pycairo/) | Graphics | Binding | "Cairo is a 2D (vector) graphics library ... (that) provides operations similar to the drawing operators of PostScript and PDF. Operations in cairo including stroking and filling cubic Bézier splines, transforming and compositing translucent images, and antialiased text rendering. All drawing operations can be transformed by any affine transformation (scale, rotation, shear, etc.)", "Cairo is implemented as a library written in the C programming language, but bindings are available for several different programming languages." "Pycairo is a set of Python bindings ..." Cairo can write to the [Linux framebuffer](http://lists.cairographics.org/archives/cairo/2010-July/020378.html). |
| [terminal](http://blog.daum.net/nskystars/2644517) | Terminal | Source | "A Simple Linux Framebuffer Terminal in Python (and C)" using the  [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) discussed above | 
| [tinywm](http://incise.org/tinywm.html) | Window manager | Source | "a tiny window manager that I created as an exercise in minimalism. ... It is only around 50 lines of C. There is also a Python version using python-xlib." |
| [Qtile](http://www.qtile.org/), also [here](http://docs.qtile.org/en/latest/) and [here](https://github.com/qtile/qtile) | Window manager | Source, configuration, API, client | "Qtile is a full-featured, hackable tiling window manager written in Python." |
| [peppy](http://peppy.flipturn.org/), also [here](http://code.google.com/p/peppy/) | Editor | Wrapper, plugins | "an XEmacs-like editor in Python", "an extensible framework in Python that can support editing and viewing many different types of files, not just text files", "wrap(s) the wonderful [Scintilla](http://www.scintilla.org/) editing component", "peppy is extended by plugins. Plugins are based on the [yapsy](http://yapsy.sourceforge.net/) component architecture. |
| [Wily](http://www.cse.yorku.ca/~oz/wily/pythonpaper.html), also [here](http://www.cse.yorku.ca/~oz/wily/python.html) | Editor | Client | "Wily emulates in the Unix and X Windows environment the Acme editor from Plan 9." " Wily is an editing environment which can be extended with Python programs. Instead of using an embedded Python interpreter, Wily talks a simple message protocol, and a module lets Python speak the same protocol." |
| [buzhug](http://buzhug.sourceforge.net/) | Database | Source, query language | "a pure-Python database engine, using a Pythonic, no-SQL syntax ... The database is implemented as a Python iterator, yielding objects whose attributes are the fields defined when the base is created ; therefore, requests can be expressed as list comprehensions or generator expressions, instead of SQL queries |
| [CodernityDB](http://labs.codernity.com/codernitydb/) | Database | Source, query language | "CodernityDB is opensource, pure Python (no 3rd party dependency), fast (really fast check Speed if you don’t believe in words), multiplatform, schema-less, NoSQL database." |
| [coroutines](http://www.dabeaz.com/coroutines/) | Programming technique | Source | "...  a practical exploration of using Python coroutines (extended generators) for solving problems in data processing, event handling, and concurrent programming."  "Part 7: Writing an Operating System" includes lots of code samples. |

Key to **Python role** column

* **Source**
The component is written in Python.

* **Wrapper** 
The component is a program whose core is written in another language,
that is invoked by a Python wrapper.

* **Configuration**
The component can be configured by scripts written in Python.

* **Plugin**
The component can load Python code that extends its behavior.

* **API** 
The component provides an Application Programming Interface: Python
classes and functions that can be called from a user's 
Python program to invoke component behavior.

* **Binding** 
The component is a library written in another language,
with a Python API as an alternative to the native API.

* **Query language** 
The component is a database whose query language is provided as a Python API.

* **Client**
The component is a server that communicates using a protocol that has
a Python API.
