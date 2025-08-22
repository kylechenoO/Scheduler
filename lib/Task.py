'''
Task.py
Author Kyle
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import builtin pkgs
import os
import sys
import time
import signal
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

## import private pkgs
from Job import Job

## Task class
class Task(object):
    '''
    Task: responsible for loading jobs and executing them
    '''
    def __init__(self, config, logger):
        ## load configs
        self.config = config
        self.logger = logger

        ## init process
        self.logger.debug('[Task][init][start]')
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # systemd signals handling
        signal.signal(signal.SIGHUP, self.handle_reload)
        signal.signal(signal.SIGTERM, self.handle_exit)
        signal.signal(signal.SIGINT, self.handle_exit)
        self.logger.debug('[Task][init][end]')

    ## run_command func
    def run_command(self, cmd: str):
        '''
        Execute the job command
        '''
        self.logger.debug('[Task][run_command][start]')
        try:
            self.logger.info('[Task][run_command][%s]' % (cmd))
            ## fork subprocess to run command
            ## if cmd end with '&> /dev/null' will redirect output to /dev/null
            if cmd.endswith('&> /dev/null'):
                cmd = cmd.removesuffix('&> /dev/null').strip()
                subprocess.run(
                    cmd,
                    shell = True,
                    check = True,
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                )

            ## else get all output in console
            else:
                output = subprocess.run(
                    cmd,
                    shell = True,
                    check = True,
                    capture_output = True,
                    text = True
                )
                self.logger.info('[Task][run_command][stdout][%s]' % (output.stdout.strip()))
                self.logger.info('[Task][run_command][stderr][%s]' % (output.stderr.strip()))

        except Exception as e:
            self.logger.error('[Task][Job failed: %s, Error: %s]' % (cmd, e))

        self.logger.debug('[Task][run_command][end]')

    ## load_jobs func
    def load_jobs(self):
        '''
        Load jobs from config
        '''
        ## remove jobs
        for job in self.scheduler.get_jobs():
            self.scheduler.remove_job(job.id)

        ## trigger jobs
        for job in self.config.jobs:
            ## get job
            trigger = CronTrigger(
                second = job.second,
                minute = job.minute,
                hour = job.hour,
                day = job.day,
                month = job.month,
                day_of_week = job.day_of_week
            )

            ## add job to task
            self.scheduler.add_job(
                self.run_command,
                trigger,
                args=[job.command],
                id=job.id,
                name=job.command,
                replace_existing=True,
                max_instances=100,
                coalesce=False
            )

            self.logger.debug('[LoadJob][%s][%s]' % (job.command, trigger))

    ## list_jobs func
    def list_jobs(self):
        '''
        List all scheduled jobs
        '''
        ## get current jobs
        jobs = self.scheduler.get_jobs()

        ## if no jobs found
        if not jobs:
            self.logger.info('[ListJobs][No jobs currently scheduled]')

        ## load & prt jobs details
        else:
            self.logger.info('[Current Jobs]')
            for job in jobs:
                self.logger.info('[ID=%s][Name=%s][NextRunTime=%s][Trigger=%s]' % (job.id, job.name, job.next_run_time, job.trigger))

    ## handle_reload func
    def handle_reload(self, signum, frame):
        '''
        Handle systemd reload (SIGHUP)
        '''
        self.logger.info('[Signal][Reloading config and jobs...]')

        ## load configs
        self.config.load()

        ## load jobs
        self.load_jobs()

        ## prt jobs
        self.list_jobs()

    ## handle_exit func
    def handle_exit(self, signum, frame):
        '''
        Handle systemd stop (SIGTERM/SIGINT)
        '''
        self.logger.info('[Signal][Stopping Scheduler...]')
        self.scheduler.shutdown(wait = False)
        sys.exit(0)

    ## run func
    def run(self):
        '''
        Main loop
        '''
        ## load configs
        self.config.load()

        ## load jobs
        self.load_jobs()

        ## prt current jobs
        self.list_jobs()

        ## main loop
        while True:
            ## reload jobs if config changes
            if self.config.changed():
                self.logger.info('[Config Updated][Reloading jobs...]')

                ## reload configs
                self.config.load()

                ## reload jobs
                self.load_jobs()

                ## prt current jobs
                self.list_jobs()

            ## wait for next sec
            time.sleep(1)
