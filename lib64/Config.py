'''
Config.py
Author Kyle
Version 20250822v1
Email kyle@hacking-linux.com
'''
# import buildin pkgs
import os
import re
import sys
import json
import configparser
from pathlib import Path

## Config Class
class Config(object):
    ## initial function
    def __init__(self, workpath):
        '''
        Load cfgs from etc/global.conf
        '''
        ## get workpath
        self.workpath = workpath

        ## set config file point
        global_filepath = '%s/etc/global.conf' % (self.workpath)
        configParserObj = configparser.ConfigParser()
        configParserObj.read(global_filepath)
        
        ## load modules args
        ## log configs
        self.LOG_DIR = configParserObj.get('LOG', 'LOG_DIR')
        self.LOG_DIR = '%s/%s' % (self.workpath, self.LOG_DIR)
        self.LOG_FILE = configParserObj.get('LOG', 'LOG_FILE')
        self.LOG_FILE = '%s/%s' % (self.LOG_DIR, self.LOG_FILE)
        self.LOG_LEVEL = configParserObj.get('LOG', 'LOG_LEVEL').upper()
        self.LOG_MAX_SIZE = int(
            configParserObj.get(
                'LOG', 'LOG_MAX_SIZE')) * 1024 * 1024
        self.LOG_BACKUP_COUNT = int(
            configParserObj.get(
                'LOG', 'LOG_BACKUP_COUNT'))

        ## lock configs
        self.LOCK_DIR = configParserObj.get('LOCK', 'LOCK_DIR')
        self.LOCK_DIR = '%s/%s' % (self.workpath, self.LOCK_DIR)
        self.LOCK_FILE = configParserObj.get('LOCK', 'LOCK_FILE')
        self.LOCK_FILE = '%s/%s' % (self.LOCK_DIR, self.LOCK_FILE)

        ## job configs
        self.JOBS_CFG = configParserObj.get('JOBS', 'JOBS_CFG')
        self.JOBS_CFG = '%s/etc/%s' % (self.workpath, self.JOBS_CFG)

        ## initial dirs
        self.dirInit(self.LOG_DIR)

    ## directory initial function
    def dirInit(self, fn):
        '''
        Init dir
        '''
        ## mkdir if not existed
        if not os.path.exists(fn):
            try:
                os.mkdir(fn)

            ## error handling
            except Exception as e:
                sys.stderr.write('[Error][%s]' % (e))
                sys.stderr.flush()

        ## return
        return(True)
