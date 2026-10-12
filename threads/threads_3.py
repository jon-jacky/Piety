# threads_3.phy - explanation in threads_3.txt.  To run:
#
# ...$ python3 -im ted
# >> import threads_3

from frame import e, o2, on
import pyshell
from timers import Timer
from writer import Writer
import threading
from threading import Thread
threads = threading.enumerate
from pyshell import ted

o2()
e('a.txt')
ta = Timer()
abuf = Writer('a.txt')
Thread(target=ta.timer,args=(1000,1,'A',abuf)).start()
on()
ted()

