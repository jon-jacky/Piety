
Python language summaries:

- [Comprehensive Python Cheatsheet](https://gto76.github.io/python-cheatsheet/)
  Compact languge summary.
- [Python Mastery](https://github.com/dabeaz-course/python-mastery/blob/main/PythonMastery.pdf)
  500+ slides from a four day 
  [course](https://github.com/dabeaz-course/python-mastery).
  PDF, best to download and read offline.

Language processors for Python and/or in Python:
 
| System | Type | Description |
| --------- | ---- | ----------- |
| [CPython](https://github.com/python/cpython/tree/3.11) | Interpreter, compiler | Source code for reference Python language implementation from python.org. Choose the Python version from the branch button near the upper left corner of the page. |
| [CPython Directory structure](https://devguide.python.org/getting-started/setup-building/index.html#directory-structure)  | Documentation | Contents of the source code directories (above), from the [Developer's Guide](https://devguide.python.org/) |
| [CPython Internals](https://www.youtube.com/playlist?list=PLV7iu6GiDKwQWZbapY5mPEQa0V1OgC358)  | Lectures | 10 hours of video (2008, Python 2) | 
| [History of Python](https://python-history.blogspot.com/2009/01/pythons-design-philosophy.html) | Blog | Series of blog posts by Python creator Guido Van Rossum |
| [Minimal Python](https://snarky.ca/tag/syntactic-sugar/) | Blog posts, with code  | "I had set out to find ... this core set of (Python) syntax. ... If you can implement this subset ... you can do a syntactic translation to support  the rest of Python ..." |
| [Tested Semantics for Python](https://cs.brown.edu/~sk/Publications/Papers/Published/pmmwplck-python-full-monty)  | Research paper, abstract and links to full PDF and software | "We present a small-step operational semantics for the Python programming language. We present both a core language for Python, suitable for tools and proofs, and a translation process for converting Python source to this core. We have tested ... the core for conformance with the primary Python implementation ... |
| [Reverse-Engineering Python](http://pages.cpsc.ucalgary.ca/~aycock/papers/ucpy.pdf), also  [here](http://pages.cpsc.ucalgary.ca/~aycock/papers/mamba.pdf) | Compiler, assembler/linker, virtual machine | UCPy compiler, targeting Python 1.5.2 with some 2.x in 2002.  "Our new virtual machine ... *mamba* has 19 instructions compared to CPython's 103 instructions." "This reduction ... is accomplished by removing functionality from instructions and relocating that functionality into objects ..." |
| [Python Compilation/Interpretation Process](https://stackoverflow.com/questions/3299648/python-compilation-interpretation-process?rq=1)  | Documentation | Includes explanation of disassembled bytecode |
| [Python Language Services](https://docs.python.org/3.11/library/language.html) | Compiler components, API, etc. | "modules to assist in working with the Python language. These modules support tokenizing, parsing, syntax analysis, bytecode disassembly, and various other facilities. From the [Python Standard Library](http://docs.python.org/3.11/library/index.html).|  
| [py_compile](https://docs.python.org/3.11/library/py_compile.html) | Python to bytecode compiler | "provides a function to generate a byte-code file from a source file ..." From Python Language Services (above). | 
| [Tailbiter](https://codewords.recurse.com/issues/seven/dragon-taming-with-tailbiter-a-bytecode-compiler) | Python to bytecode compiler | "... a small compiler able to compile itself ... in and for a subset of Python 3 ... I wrote this to accompany (the Byterun bytecode interpreter below) which takes the output of a compiler and executes it"|
| [Byterun](https://github.com/nedbat/byterun), also [blog post](http://nedbatchelder.com/blog/201301/byterun_and_making_cells.html). | Bytecode interpreter | "a pure-Python implementation of a Python bytecode execution virtual machine". More about Python bytecodes [here](http://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html) |
| [Python in Python](http://aosabook.org/en/500L/a-python-interpreter-written-in-python.html) | Bytecode Interpreter | "Byterun (above) is a compact Python interpreter that's easier to understand than CPython. ..." |
| [Pythoniac](https://mail.python.org/pipermail/python-list/2002-June/152587.html) and [here](https://mail.python.org/pipermail/python-list/2002-June/163423.html), also [here](https://groups.google.com/forum/#!msg/comp.lang.python/paIIR2LJ2aI/QT0l0EWk2SUJ) | Bytecode interpreter in hardware (ideas, discussion) | "The PVM (Python Virtual Machine) processes objects (via pointers on the stack), which are treated in a 'black box' fashion - i.e. they have add, subtract, compare etc. methods that are called by the PVM ... These methods of objects may not actually be coded for in Python ... the PVM is unaware, in the majority of cases, of what actually needs to be done to manipulate objects, it just makes calls to non Python code. ... how to go about dealing with this in a Python processor? |
| [pyCPU](http://pycpu.wordpress.com/), also [here](http://sourceforge.net/projects/pycpu/) | Bytecode interpreter for FPGA | "an implementation of a hardware CPU in [myHDL](http://www.myhdl.org). The CPU can directly execute something very similar to python bytecode (but only a very restricted instruction set).", "Running a very small subset of Python on an FPGA is possible." |
| [assembler](http://pythonwise.blogspot.com/2012/06/python-based-assembler.html) | Assembler | "the assembly (source) file is actually a Python file (module)" where statements such as *load(r2, MEM_LOC1)* are Python calls |
| [machine code](http://multigrad.blogspot.com/2014/07/low-level-frenzy.html) | Execute opcodes | "... execute arbitrary x86-64 instructions in Python ... write a byte string that contains the executable code and then cast it into a CFUNCTYPE object." |
| [Python internals](https://eli.thegreenplace.net/tag/python-internals) | Blog posts with code | For example, "I recently had to do a lot of binary data processing in memory ... made me think about the most efficient way to read data from a file into a modifiable memory chunk ..." |
| [Repy](https://seattle.poly.edu/wiki/ProgrammersPage), also [here](https://seattle.poly.edu/wiki/UnderstandingSeattle/CodeSafety) and [here](https://github.com/SeattleTestbed/repy_v2) | Python subset, sandboxed VM | "Restricted Python" language, runtime, sandboxed VM for writing distributed computing applications for the [Seattle testbed](https://seattle.poly.edu/html/) |
| [Pygments](http://pygments.org/) | Syntax highlighter | "syntax highlighting engine engine written in Python ... take source code (or other markup) in a supported language and output ... syntax highlighting markup" |
| [Awesome Python Compilers](https://github.com/pfalcon/awesome-python-compilers) | Annotated links | Historical survey of Python compilers, with links to many mentioned below |
| [LPython](https://lpython.org/)  | Annotated links | Bottom of page has links to 32 Python compilers. LPython itself is a compiler for Python with type annotations. |
| [PyPy](http://pypy.org/), also [here](http://www.aosabook.org/en/pypy.html)  | Interpreter, translator, JIT compiler | "a fast, compliant alternative implementation of the Python language (2.7.3)." "... except for a negligible number of C stubs, is written completely in Python."  Not compatible with extensions written for CPython; they must be ported.  Bytecode interpreter [here](http://pypy.readthedocs.org/en/latest/interpreter.html).  Nice summary [here](https://news.ycombinator.com/item?id=6708867).  Brief explanation [here](https://news.ycombinator.com/item?id=11522767).  Video about experimenter's experiences [here](http://www.youtube.com/watch?v=l_HBRhcgeuQ). |
| [PyPy.js](http://www.rfk.id.au/blog/entry/pypy-js-first-steps/), also [here](https://news.ycombinator.com/item?id=6090041) | Python-to-Javascript compiler | " have the RPython toolchain (from PyPy) compile things down to C code; compile the C code to JavaScript using Emscripten".  The page also discusses other Python-to-Javascript systems including *Skulpt*, *Brython*, *Pyjamas*, and *repl.it* |
| [Micro Python](http://micropython.org/), also [here](https://github.com/micropython/micropython) | Compiler, runtime | "complete rewrite, from scratch, of Python. ...  includes a complete parser, compiler, virtual machine, runtime system, garbage collector and support libraries to run on a microcontroller", "32-bit ARM ... tested on an STM32F405 chip"" |
| [Cython](http://cython.org/), also [HN](https://news.ycombinator.com/item?id=6114334), also [blog](http://honnibal.wordpress.com/2014/10/21/writing-c-in-cython/) and [more HN](https://news.ycombinator.com/item?id=8483872) | Optimizing compiler, C extensions | "Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language. ... a superset of the Python language that additionally supports calling C functions and declaring C types on variables and class attributes. This allows the compiler to generate very efficient C code from Cython code ... makes Cython the ideal language for wrapping external C libraries ... and for fast C modules that speed up the execution of Python ...".  Only works with CPython.  |
| [Pyston](https://tech.dropbox.com/2014/04/introducing-pyston-an-upcoming-jit-based-python-implementation/), also [here](https://github.com/dropbox/pyston) | Compiler | "a new, under-development Python implementation built using LLVM and modern JIT techniques with the goal of achieving good performance" |
| [Unladen Swallow](https://code.google.com/p/unladen-swallow/wiki/ProjectPlan), outcome [here](http://legacy.python.org/dev/peps/pep-3146/) | Compiler | CPython branch ca. 2009 aiming at "a performance improvement of 5x ...".  The goal was not met. Relevant background literature [here](https://code.google.com/p/unladen-swallow/wiki/RelevantPapers). |
| [gccpy](http://gcc.gnu.org/wiki/PythonFrontEnd), also [here](https://github.com/redbrain/gccpy) and [here](http://redbrain.co.uk/compiling-python-with-gccpy/) | Compiler | "compile Python Code as an AOT (ahead of time) compiled language",  "a python front end to GCC" |
| [Replicant](https://github.com/soundspectrum/replicant) | Compiler | "LLVM-based Python compiler and execution environment with a focus on performance, no-GIL threading, embeddability, and extensibility." | 
| [Numba](http://numba.pydata.org/) | Compiler | "just-in-time specializing compiler which compiles annotated Python and NumPy code to LLVM (through decorators) ... produce optimized native code ... integrate with native foreign languages" |
| [Falcon](http://www.phi-node.com/2013/06/how-fast-can-we-make-interpreted-python.html), also [here](http://arxiv.org/abs/1306.6047) and [here](https://github.com/rjpower/falcon) | Optimized interpreter | ".. a high-performance bytecode interpreter fully compatible with the standard CPython interpreter. ... does not replace the standard CPython interpreter, but rather runs inside of it ... 25% faster than the standard Python interpreter on most benchmarks and in some cases about 2.5X faster."  The [paper](http://arxiv.org/abs/1306.6047) discusses CPython internals and the [Hacker News discussion](https://news.ycombinator.com/item?id=5943258) (also [here](https://news.ycombinator.com/item?id=11522767)) has some interesting comments on Python design and performance. |
| [numpile](http://dev.stephendiehl.com/numpile/), also [github](https://github.com/sdiehl/numpile) and [slides](http://dev.stephendiehl.com/cfa/slides.pdf) | LLVM Optimized Python | "LLVM-based numeric specializer for scientific Python code", "generate machine code at runtime in Python! Now we'll use the LLVM JIT to actually actually execute the code and interchange values between the CPython runtime and the LLVM JIT" | 
| [pyast64](https://benhoyt.com/writings/pyast64/), also [github](https://github.com/benhoyt/pyast64) and [HN](https://news.ycombinator.com/item?id=14644576) | Compiler | "Python 3 program that compiles a subset of the Python AST to x64-64 assembler. It's extremely restricted (read "a toy") but it's a nice proof of concept" |
| [hython](https://github.com/mattgreen/hython), also [blog](http://callcc.io/hython-the-simplest-possible-language/) | Compiler | "Python 3 interpreter written in Haskell. I'm new to Haskell, so this will move pretty slowly." (begun Jul 2014) |
| [abrvalg](https://github.com/akrylysov/abrvalg) | Interpreter | "Python-like programming language interpreter written in Python" |
| [cffi](http://cffi.readthedocs.org/en/latest/index.html), also [blog](http://morepypy.blogspot.com/2012/08/cffi-release-03.html) and [example](http://www.mindtribe.com/2015/10/using-cffi-to-debug-from-python/) | FFI for PyPy | "Foreign Function Interface for Python calling C code. The aim of this project is to provide a convenient and reliable way of calling C code from Python. The interface is based on LuaJIT’s FFI. ... The goal is to call C code from Python. You should be able to do so without learning a 3rd language: every alternative requires you to learn their own language (Cython, SWIG) or API (ctypes)."  From the PyPy project, works with CPython |
| [pycparser](https://github.com/eliben/pycparser) | C parser | "Complete C99 parser in pure Python", used by *cffi* (above) |
| [inlinec](https://github.com/georgek42/inlinec), also [HN](https://news.ycombinator.com/item?id=22219696) | Compiler ? | "write inline C functions in Python source code", demos interpreter/compiler techniques |
| [lptrace](https://github.com/khamidou/lptrace), also [here](http://khamidou.com/lptrace/) | Debugging tool | "lets you see in real-time what functions a Python program is running ... thank the [Pyrasite](https://github.com/lmacken/pyrasite) project for coming up with the idea to inject code into a running Python process." |
| [python-goto](https://github.com/snoack/python-goto), also [HN](https://news.ycombinator.com/item?id=10250770) | Language extension for CPython | "A function decorator, that rewrites the bytecode, to enable goto in Python", "label .begin and goto .begin is regular Python syntax to retrieve the attribute begin from the objects with the variable names label and goto", "a fun exercise to understand the internals of CPython" |
| [toy compiler](http://www.jroller.com/languages/entry/python_writing_a_compiler_and) | Educational exercise | "Compiler and Interpreter in 160 lines of code ... for a simple 'while' language."  Tiny but informative example (target language is not Python). |
| [Lispy](https://www.norvig.com/lispy.html) | Scheme | "an interpreter for most of the Scheme dialect of Lisp using Python 3 as the implementation language" |
| [Hy](http://docs.hylang.org/en/latest/), also [github](https://github.com/hylang/hy) and [blog](https://velox.pw/hy/2014/01/17/the-state-of-hy.html) and [another blog](http://dustycloud.org/blog/how-hy-backported-yield-from-to-python2/) and [HN](https://news.ycombinator.com/item?id=8641126) | Lisp | ""Hy is a LISP leeching^H^H^H^H^H living off the Python world. It compiles down to Python’s AST and is completely bidirectional, you can import Hy into Python and vica versa seamlessly!" |
| [lisp.py](https://thinkpython.blogspot.com/2008/02/lisp-in-single-expression.html)  | Lisp | "An interpreter for a simple scheme like lexically scoped language implemented as single python expression." |
| [l.py](http://flownet.com/ron/lisp/l.py) | Lisp | "A tiny interpreter for a lisp-like language with full lexical closures in Python", less than 100 lines |
| [Lisp compiler](https://github.com/jbush001/LispMicrocontroller/blob/master/compile.py) | Lisp | Compiler for a custom "simple microcontroller that runs a compiled LISP dialect" |
| [pixie](https://github.com/pixie-lang/pixie), also [HN](https://news.ycombinator.com/item?id=8480608) | Lisp | "a lightweight Lisp ... inspired by Clojure ... written in RPython" |

Revised May 2024
 