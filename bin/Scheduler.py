'''
Scheduler.py
Author Kyle Chen
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import buildin pkgs
import re
import os
import sys
import time

## get workpath
workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

## append workpath to path
sys.path.append('%s/lib' % (workpath))

## import private pkgs
from Log import Log
from Job import Job
from Lock import Lock
from Task import Task
from Config import Config
from JobConfig import JobConfig

## Scheduler Class
class Scheduler(object):
    ## init func
    def __init__(self):
        '''
        Init Scheduler Process
        '''
        ## set vars
        self.config = Config(workpath)
        self.pid = os.getpid()
        self.pname = 'Scheduler.py'

        ## init logger
        logObj = Log('Scheduler', self.config)
        self.logger = logObj.getLogger()

        ## load global.conf
        self.logger.info('[init][Start]')
        self.logger.debug('[LOG_DIR][%s]' % (self.config.LOG_DIR))
        self.logger.debug('[LOG_FILE][%s]' % (self.config.LOG_FILE))
        self.logger.debug('[LOG_LEVEL][%s]' % (self.config.LOG_LEVEL))
        self.logger.debug('[LOG_MAX_SIZE][%s]' % (self.config.LOG_MAX_SIZE))
        self.logger.debug( '[LOG_BACKUP_COUNT][%s]' % (self.config.LOG_BACKUP_COUNT))
        self.logger.debug('[LOCK_DIR][%s]' % (self.config.LOCK_DIR))
        self.logger.debug('[LOCK_FILE][%s]' % (self.config.LOCK_FILE))
        self.logger.debug('[JOBS_CFG][%s]' % (self.config.JOBS_CFG))
        self.logger.info('[init][End]')

        ## init lock
        self.lock = Lock(self.config, logger=self.logger)
        if not self.lock.acquire():
            self.logger.error('[Another Scheduler is already running][exit]')
            sys.exit(-1)

    ## run func
    def run(self):
        '''
        Run Process
        '''
        self.logger.info('[Start]')
        ## init JobConfigObj
        JobConfigObj = JobConfig(self.config.JOBS_CFG, self.logger)

        ## init TaskObj
        TaskObj = Task(JobConfigObj, self.logger)

        ## TaskObj run
        TaskObj.run()

        self.logger.info('[End]')
        return(True)

## main run part
if __name__ == '__main__':
    '''
    Gen SchedulerObj & run
    '''
    SchedulerObj = Scheduler()
    SchedulerObj.run()
