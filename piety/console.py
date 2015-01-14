"""
console.py - Manage multiple terminal applications (jobs) in one Piety task

"""

def Console(object):

    def __init__(self):
        'Initialize collection of jobs'
        pass
    
    def add(self, job):
        'Add a job to the collection'
        pass

    # not yet any need for del(self, job)
    
    def jobs(self):
        'List jobs'
        pass

    def run(self, job):
        'Give focus to this job and run it (put it in the foreground)'
        pass

    def stop(self, job):
        'Stop this job and remove focus (put it in the background)'
        pass
