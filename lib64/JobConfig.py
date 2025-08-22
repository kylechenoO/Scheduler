'''
JobConfig.py
Author Kyle
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import builtin pkgs
import re
import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

## import private pkgs
from Job import Job

## JobConfig class
class JobConfig(object):
    '''
    Responsible for reading and parsing the config file
    Format: second minute hour day month day_of_week command
    '''
    ## __init__ func
    def __init__(self, filepath, logger):
        ## load configs
        self.logger = logger
        self.logger.debug('[JobConfig][init][start]')
        self.filepath = filepath
        self.last_mtime = None
        self.jobs: list[Job] = []
        self.logger.debug('[JobConfig][init][end]')

    ## load func
    def load(self) -> list[Job]:
        '''
        Read config file and parse jobs
        '''
        ## create file if file not existed
        if not os.path.exists(self.filepath):
            self.logger.warning('[JobConfig][Config file not found: %s]' % (self.filepath))
            self.logger.info('[JobConfig][creating new %s][start]' % (self.filepath))
            Path(self.filepath).touch()
            self.logger.info('[JobConfig][creating new %s][end]' % (self.filepath))

        ## get jobs from cfg file
        jobs = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            ## handle it by lines
            for idx, raw_line in enumerate(f, 1):
                line = raw_line.strip()

                ## skip '#' lines
                if not line or line.startswith('#'):
                    continue

                self.logger.debug('[Config][Loading][%s]' % (line))

                ## split the line
                parts = line.split()

                ## if len < 7 print eror msg and skip to next line
                if len(parts) < 7:
                    self.logger.error('[Config Error] Line %s: %s' % (idx, line))
                    continue

                ## load current line to items
                second, minute, hour, day, month, day_of_week = parts[:6]
                command = ' '.join(parts[6:])
                command = command.strip().rstrip()

                ## load current line as Job object
                jobs.append(Job(
                    id='job_%s' % (idx),
                    second = second,
                    minute = minute,
                    hour = hour,
                    day = day,
                    month = month,
                    day_of_week = day_of_week,
                    command = command
                ))

        self.jobs = jobs

        ## return
        return(jobs)

    ## changed func
    def changed(self) -> bool:
        '''
        Check if config file has been modified
        '''
        self.logger.debug('[Config][ChangedCheck][start]')
        ret = False
        ## get current filepath
        try:
            mtime = os.path.getmtime(self.filepath)
            self.logger.debug('[Config][ChangedCheck][Checking]')

        ## error handling
        except FileNotFoundError:
            self.logger.error('[Config][ChangedCheck][FileNotFoundError]')
            ret = False

        ## update self.last_mtime if not matched
        if self.last_mtime is None or mtime != self.last_mtime:
            self.logger.info('[Config][ChangedCheck][Change detacted]')
            self.last_mtime = mtime
            ret = True

        self.logger.debug('[Config][ChangedCheck][end]')

        ## return
        return(ret)
