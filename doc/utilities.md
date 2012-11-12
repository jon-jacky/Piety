Here are some examples of system software and utilities written in
Python, or programmable in Python.

| Component | Type | Python role | Description |
| --------- | ---- | ----------- | ----------- |
| [coroutines](http://www.dabeaz.com/coroutines/) | Programming technique | Source | "...  a practical exploration of using Python coroutines (extended generators) for solving problems in data processing, event handling, and concurrent programming."  "Part 7: Writing an Operating System" includes lots of code samples. |
| [TCPStack](https://github.com/dound/vns/blob/master/TCPStack.py) | Network | Source | Lightweight TCP stack.  Part of [VNS](http://yuba.stanford.edu/vns/), the "Virtual Network System for teaching and experimentation" (also [here](http://yuba.stanford.edu/vns/files/pub/vns_sigcse.pdf)). |
| [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) | Graphics | Source | "Drawing to the Linux Framebuffer in Python" Writes to /dev/fb0 using fcntl, mmap, struct.  Looks like a general technique for doing low-level I/O in Linux.  Based on C code [here](http://doc.qt.digia.com/3.0/emb-framebuffer-howto.html), but simpler. |
| [Python X Library](http://python-xlib.sourceforge.net/) | Graphics | Source | "a fully functional X client library for Python programs. It is written entirely in Python, in contrast to earlier X libraries for Python (the ancient X extension and the newer plxlib) which were interfaces to the C Xlib." |
| [PyCairo](http://www.tortall.net/mu/wiki/CairoTutorial), also [here](http://cairographics.org/pycairo/) | Graphics | Binding | "Cairo is a 2D (vector) graphics library ... (that) provides operations similar to the drawing operators of PostScript and PDF. Operations in cairo including stroking and filling cubic Bézier splines, transforming and compositing translucent images, and antialiased text rendering. All drawing operations can be transformed by any affine transformation (scale, rotation, shear, etc.)", "Cairo is implemented as a library written in the C programming language, but bindings are available for several different programming languages." "Pycairo is a set of Python bindings ..." Cairo can write to the [Linux framebuffer](http://lists.cairographics.org/archives/cairo/2010-July/020378.html). |
| [tinywm](http://incise.org/tinywm.html) | Window manager | Source | "a tiny window manager that I created as an exercise in minimalism. ... It is only around 50 lines of C. There is also a Python version using python-xlib." |
| [Qtile](http://www.qtile.org/), also [here](http://docs.qtile.org/en/latest/) and [here](https://github.com/qtile/qtile) | Window manager | Source, Client | "Qtile is a full-featured, hackable tiling window manager written in Python." |
| [uzbl](http://uzbl.org/), also [here](https://github.com/Dieterbe/uzbl) | Browser | Wrapper | "Uses WebKitGtk+ for rendering and network interaction", "Uses a set of scripts (mostly Python) ... so things work out of the box; yet plenty of room for customization."  |
| [terminal](http://blog.daum.net/nskystars/2644517) | Terminal | Source | "A Simple Linux Framebuffer Terminal in Python (and C)" using the techniques above | 
| [peppy](http://peppy.flipturn.org/) | Editor | Wrapper | "an XEmacs-like editor in Python", "wrap(s) the wonderful [Scintilla](http://www.scintilla.org/) editing component" |
| [Wily](http://www.cse.yorku.ca/~oz/wily/pythonpaper.html), also [here](http://www.cse.yorku.ca/~oz/wily/python.html) | Editor | Client | "Wily emulates in the Unix and X Windows environment the Acme editor from Plan 9." " Wily is an editing environment which can be extended with Python programs. Instead of using an embedded Python interpreter, Wily talks a simple message protocol, and a module lets Python speak the same protocol." |

Key to **Python role** column

* **Source**
The component is written in Python.  It can be extended by revising or
adding to the Python source.

* **Binding** 
The component is a library written in another language,
with a Python API as an alternative to the native API, so the library
can be easily used by Python programs.

* **Wrapper** 
The component is a program whose core is written in another language,
that is invoked by a Python wrapper.  The program can be scripted or 
customized in Python.

* **Client**
The component is a server written in another language that
communicates using a protocol that has a Python API, so the server can
be easily used by Python programs.
