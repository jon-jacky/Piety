# Code for demo described in threads_2.txt.
# To run this code, first at the system command line:
# ...$ . ~/Piety/bin/paths
# ...$ python3 -im tm
# Then a window and the pysh prompt >> appears.  At the psyh prompt:
# >> import threads_2
# Then a.txt and b.txt windows appear, with timer messages from each thread
# >> from threads_2 import *
# Now you can type commands described in threads_2.txt to control timers etc.
# >> threads()
# >> ta.delay = 0.5
# ... etc. ...

from edsel import e, o2
from timers import Timer
from writer import Writer
import threading
from threading import Thread
threads = threading.enumerate

e('a.txt')
o2()
e('b.txt')

ta = Timer()
tb = Timer()

abuf = Writer('a.txt')
bbuf = Writer('b.txt')
 
Thread(target=tb.timer,args=(1000,1,'B',bbuf)).start()
Thread(target=ta.timer,args=(1000,1,'A',abuf)).start()

