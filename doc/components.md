
Here are examples of systems software that is written in Python, or is programmable in Python.

| Component | Role | Description |
| --------- | ---- | ----------- |
| [PyPy](http://pypy.org/), also [here](http://www.aosabook.org/en/pypy.html)  | Source | "a Python implementation and a dynamic language implementation framework. ... PyPy, except for a negligible number of C stubs, is written completely in Python." |
| [cffi](http://cffi.readthedocs.org/en/latest/index.html), also [here](http://morepypy.blogspot.com/2012/08/cffi-release-03.html) | Source | "Foreign Function Interface for Python calling C code. The aim of this project is to provide a convenient and reliable way of calling C code from Python. The interface is based on LuaJIT’s FFI. ... The goal is to call C code from Python. You should be able to do so without learning a 3rd language: every alternative requires you to learn their own language (Cython, SWIG) or API (ctypes)."  From the PyPy project. |
| [coroutines](http://www.dabeaz.com/coroutines/) | Source | "...  a practical exploration of using Python coroutines (extended generators) for solving problems in data processing, event handling, and concurrent programming."  "Part 7: Writing an Operating System" includes lots of code samples. |
| [TCPStack](https://github.com/dound/vns/blob/master/TCPStack.py) | Source | Lightweight TCP stack.  Part of [VNS](http://yuba.stanford.edu/vns/), the "Virtual Network System for teaching and experimentation" (also [here](http://yuba.stanford.edu/vns/files/pub/vns_sigcse.pdf)). |
| [Linux Framebuffer](http://blog.daum.net/nskystars/2626663) | Source | "Drawing to the Linux Framebuffer in Python" Writes to /dev/fb0 using fcntl, mmap, struct.  Looks like a general technique for doing low-level I/O in Linux.  Based on C code [here](http://doc.qt.digia.com/3.0/emb-framebuffer-howto.html), but simpler. |
| [terminal](http://blog.daum.net/nskystars/2644517) | Source | "A Simple Linux Framebuffer Terminal in Python (and C)" using the techniques above | 
| [Python X Library](http://python-xlib.sourceforge.net/) | Source | "a fully functional X client library for Python programs. It is written entirely in Python, in contrast to earlier X libraries for Python (the ancient X extension and the newer plxlib) which were interfaces to the C Xlib." |
| [tinywm](http://incise.org/tinywm.html) | Source | "a tiny window manager that I created as an exercise in minimalism. ... It is only around 50 lines of C. There is also a Python version using python-xlib." |
| [PyCairo](http://www.tortall.net/mu/wiki/CairoTutorial), also [here](http://cairographics.org/pycairo/) | Binding | "Cairo is a 2D (vector) graphics library ... (that) provides operations similar to the drawing operators of PostScript and PDF. Operations in cairo including stroking and filling cubic Bézier splines, transforming and compositing translucent images, and antialiased text rendering. All drawing operations can be transformed by any affine transformation (scale, rotation, shear, etc.)", "Cairo is implemented as a library written in the C programming language, but bindings are available for several different programming languages." "Pycairo is a set of Python bindings ..." Cairo can write to the [Linux framebuffer](http://lists.cairographics.org/archives/cairo/2010-July/020378.html). |
| [peppy](http://peppy.flipturn.org/) | Wrapper |  "an XEmacs-like editor in Python", "wrap(s) the wonderful [Scintilla](http://www.scintilla.org/) editing component" |
| [Wily](http://www.cse.yorku.ca/~oz/wily/pythonpaper.html), also [here](http://www.cse.yorku.ca/~oz/wily/python.html) | Client | "Wily emulates in the Unix and X Windows environment the Acme editor from Plan 9." " Wily is an editing environment which can be extended with Python programs. Instead of using an embedded Python interpreter, Wily talks a simple message protocol, and a module lets Python speak the same protocol." |

Key to **Role** column

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
