'''
Log.py
Author Kyle Chen
Version 20250822v1
Email kyle@hacking-linux.com
'''
## import builtin pkgs
import os
import logging
from logging.handlers import RotatingFileHandler

## Log class
class Log(object):
    def __init__(self, name, config):
        '''
        Load cfgs
        '''
        self.name = name
        self.config = config
        self.logger = self.init(self.config)

    def init(self, config):
        '''
        Init logger
        '''
        logger = logging.getLogger(self.name)

        try:
            log_level = getattr(logging, config.LOG_LEVEL)

        except AttributeError:
            log_level = logging.NOTSET

        logger.setLevel(log_level)

        # file handler
        fh = RotatingFileHandler(
            config.LOG_FILE,
            mode = 'a',
            maxBytes = config.LOG_MAX_SIZE,
            backupCount = config.LOG_BACKUP_COUNT
        )

        fh.setLevel(log_level)

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        # formatter
        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
        )

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        ## avoid multi reg
        if not logger.handlers:
            logger.addHandler(fh)
            logger.addHandler(ch)

        ## return
        return(logger)

    def getLogger(self):
        '''
        Get Logger Object
        '''
        return(self.logger)
