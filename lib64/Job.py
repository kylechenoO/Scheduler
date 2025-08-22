'''
Job.py
Author Kyle
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import builtin pkgs
from dataclasses import dataclass

@dataclass
class Job(object):
    '''
    The scheduled job entry
    '''
    id: str
    second: str
    minute: str
    hour: str
    day: str
    month: str
    day_of_week: str
    command: str
