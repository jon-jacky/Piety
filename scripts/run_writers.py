"""
run_writers.py - Run the three jobs created by session.py,
  concurrently with the two writer tasks created by writers.py,
  using the Piety scheduler.   

Start the script and run the three jobs, much as described in the header
to session.py.  You can use these three jobs at the same time the writers
are writing.

At startup, the Python interpreter runs.  Other jobs must
be prefixed by the session module name:

...$ python3 -m run_writers
>> import datetime
>> session.ed()
e README.md
... edit README.md ...
:q 
>> ...
...

View the activity of the two writer tasks by opening two terminal
windows.  In the first, type the command:: tail -f w0.txt, in the 
second type tail -f w1.txt.   A message appears in w0.txt every second,
in w1.txt every other second.  

Control the writer tasks from the Python interpreter:

>> piety.tasks()
  i     name  enabled              n  input            handler
  -     ----  -------              -  -----            -------
  0  session  true               280  _io.TextIOWrap   Console.handler
  1       t1  true               503  timer 1.0 s      Writer.write   
  2       t2  alternate          503  timer 1.0 s      Writer.write   
>> piety.tasks_list
[<piety.Session object at 0x101fa91d0>, <piety.Task object at 0x103050240>, <piety.Task object at 0x1030502b0>]
> piety.tasks_list[0].name
'session'
>> piety.tasks_list[1].name
't1'
>> piety.tasks_list[2].name
't2'
>> piety.tasks_list[1].enabled=piety.false
>> piety.tasks_list[2].enabled=piety.false

They both stop writing.  Change the interval:

>> piety.cycle
<module 'cycle' from '/Users/jon/Piety/piety/cycle.py'>
>> piety.cycle.period
1.0
>> piety.cycle.period=0.5
>> piety.tasks_list[1].enabled=piety.true
>> piety.tasks_list[2].enabled=writers.alternate

Both resume at twice the speed, t[2] at half the speed
of t[1].

>> piety.tasks_list[1].enabled=piety.false

stops writing

>> piety.tasks_list[1].enabled=piety.true

"""

import piety, session, writers # writers starts the writer tasks

def main():
    session.pysh()
    piety.run()

if __name__ == '__main__':
    main()
