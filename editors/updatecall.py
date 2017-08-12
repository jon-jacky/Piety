"""
updatecall.py - function to update display by making and sending an UpdateRec
                Split off from updates to avoid circular imports with frame
"""

from updates import UpdateRecord
import frame

def update(op, sourcebuf=None, buffer=None, origin=0, destination=0, 
           start=0, end=0):
    'Create an UpdateRecord record and send it to window and frame'
    update_record = UpdateRecord(op, sourcebuf=sourcebuf, buffer=buffer, 
                                 origin=origin, destination=destination, 
                                 start=start, end=end)
    frame.update(**update_record._asdict())
