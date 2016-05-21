"""
events.py - demo piety and eventloop modules
"""
import piety # piety imports eventloop
             
# piety defines task0, task1 for its own test
t0 = piety.Task(name='task 0', handler=piety.task0, input=piety.timer)
t1 = piety.Task(name='task 1', handler=piety.task1, input=piety.timer)

def main():
    # we don't need to assign piety.done because we use nevents instead
    piety.run(nevents=10) # handle 10 clock ticks and exit
    piety.tasks() # show the tasks

if __name__ == '__main__':
    main()
