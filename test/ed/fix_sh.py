#!/usr/bin/env python
# fix_sh.py
import sys
import ed
ed.e(sys.argv[1])
ed.s(1,ed.S(),'from ed import *; ed()','import ed; ed.main()',True)
ed.w()
ed.q()
