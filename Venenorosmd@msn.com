Skip to content
 
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 @therealcurlsport Sign out
Your account has been flagged.
Because of that, your profile is hidden from the public. If you believe this is a mistake, contact support to have your account status reviewed.
0
0 5 therealcurlsport/pitybas
forked from lunixbochs/pitybas
 Code  Pull requests 0  Projects 0  Wiki  Insights  Settings
a faithful TI-BASIC implementation https://www.biolytic.com/t-dna-rna-ol…
 121 commits
 2 branches
 0 releases
 2 contributors
 MIT
 Python 97.0%	 Visual Basic 3.0%
 Pull request   Compare This branch is 3 commits ahead of lunixbochs:master.
@therealcurlsport
therealcurlsport Rename DatabaseMexico.git to Veneno.DatabaseMexico.git
Latest commit ca7e15b  just now
Type	Name	Latest commit message	Commit time
git-github.com-therealcurlsport	Create SeleniumLibrary.git	14 minutes ago
pitybas	fix sub() function	3 years ago
tests	add list/mat test	4 years ago
DatabaseMexico.git	Create DatabaseMexico.git	13 minutes ago
LICENSE	add LICENSE	5 years ago
README.markdown	update README	5 years ago
Veneno.DatabaseMexico.git	Rename DatabaseMexico.git to Veneno.DatabaseMexico.git	just now
pb.py	structure cleanup	8 years ago
 README.markdown
pitybas
A working TI-BASIC interpreter, written in Python.

Currently, all .bas files in tests/ run except circle.bas (due to lack of graph screen functions)

Use pb.py -i vt100 to run programs which need a working home screen.

If you run pb.py with no filename, it launches an interactive shell.

Usage: pb.py [options] [filename]

Options:
	-h, --help        show this help message and exit
    -a, --ast         parse, print ast, and quit
	-d, --dump        dump variables in stacktrace
	-s, --stacktrace  always stacktrace
	-v, --verbose     verbose output
	-i IO, --io=IO    select an IO system: simple (default), vt100
© 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
Press h to open a hovercard with more details.
