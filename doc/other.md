Here are some examples of pertinent system software and utilities
written in languages other than Python.

| Component | Type | Language | Description|
|-----------|------|----------|------------|
| [/grub-core/fs](http://bzr.savannah.gnu.org/lh/grub/trunk/grub/files/head:/grub-core/fs/) ([via](http://ask.metafilter.com/230728/NTFS-FAT-HFS-Drowning-in-Acronyms#3339280)) | Read-only file systems | C | "The bootloader Grub 2 includes minimal, read-only drivers for a gazillion different file systems. ...  it's much simpler code than most drivers, since it's read-only. Plus, you can even run it in userland, which means you can easily attach a debugger and see exactly what's going on." |
| [Rubinius](http://rubini.us/), also [here](http://redartisan.com/2007/10/5/rubinius-getting-started) and [here](http://razzledazzle.it/1:origin-story/3:rubinius) | Interpreter/Compiler | Ruby | "The Rubinius bytecode virtual machine is written in C++, incorporating LLVM to compile bytecode to machine code at runtime. The bytecode compiler and vast majority of the core classes are written in pure Ruby."  Interesting contrast to [PyPy](http://pypy.org/). |
