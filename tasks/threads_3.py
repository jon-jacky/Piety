from edsel import e, o2, on
from pyshell import tpm
from timers import Timer
from writer import Writer
import threading
from threading import Thread
threads = threading.enumerate

o2()
e('a.txt')
ta = Timer()
abuf = Writer('a.txt')
Thread(target=ta.timer,args=(1000,1,'A',abuf)).start()
on()
tpm()

