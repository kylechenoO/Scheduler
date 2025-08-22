'''
Lock.py
Author Kyle
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import builtin pkgs
import os
import sys
import fcntl
import atexit
import signal

## Lock class
class Lock(object):
    def __init__(self, config, logger):
        '''
        Initialize Lock with config and optional logger.
        Lock file path is read from config.LOCK_FILE.
        '''
        ## load configs
        self.config = config
        self.lock_file = self.config.LOCK_FILE
        self.fp = None
        self.logger = logger
        self.logger.debug('[Lock][LOCK_FILE][%s]' % (self.config.LOCK_FILE))

    def _is_process_alive(self, pid):
        '''
        Check if a process with the given PID is still alive.
        '''
        try:
            # signal 0 does not kill the process, only checks
            os.kill(pid, 0)

        except OSError:
            return(False)

        return(True)

    def acquire(self):
        '''
        Try to acquire the lock.
        If the lock file exists, check if the PID inside is still alive.
        If alive, another Scheduler is running -> exit.
        If not alive, remove stale lock file and continue.
        If no lock file, create a new one and write current PID.
        '''
        ## check if lock_file existed
        if os.path.exists(self.lock_file):
            try:
                ## load lock_file
                with open(self.lock_file, 'r') as f:
                    old_pid = int(f.read().strip())

                ## exit if old_pid still running
                if self._is_process_alive(old_pid):
                    self.logger.error('[Lock][Scheduler already running with PID %s][exit]' % (old_pid))
                    return(False)

                ## clean lock_file if old_pid not running
                else:
                    self.logger.warning('[Lock][Stale lock detected (PID %s not alive)][cleaning]' % (old_pid))
                    os.remove(self.lock_file)
                    self.logger.warning('[Lock][Stale lock detected (PID %s not alive)][cleaned]' % (old_pid))

            ## error handling
            except Exception:
                os.remove(self.lock_file)

        ## acquire lock on lock_file
        try:
            ## write current pid to lock_file
            self.fp = open(self.lock_file, 'w')
            fcntl.flock(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.fp.write(str(os.getpid()))
            self.fp.flush()

            # ensure lock is released when process exits
            atexit.register(self.release)
            signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
            signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

            self.logger.info('[Lock][Acquired lock (PID %s)]' % (os.getpid()))

            ## return
            return(True)

        ## error handling
        except IOError:
            self.logger.error('[Lock][Failed to acquire lock: %s]' % (self.lock_file))

            ## return
            return(False)

    ## release func
    def release(self):
        '''
        Release the lock and remove the lock file.
        Called automatically at process exit if acquired.
        '''
        ## check if self.fp existed
        ret = False
        if self.fp:
            try:
                ## release the lock
                fcntl.flock(self.fp, fcntl.LOCK_UN)
                self.fp.close()
                if os.path.exists(self.lock_file):
                    os.remove(self.lock_file)

                self.logger.info('[Lock][Released lock (PID %s)]' % (os.getpid()))
                ret = True

            ## error handling
            except Exception as e:
                self.logger.error('[Lock][Failed to release lock: %s]' % (e))
                ret = False

        return(ret)

