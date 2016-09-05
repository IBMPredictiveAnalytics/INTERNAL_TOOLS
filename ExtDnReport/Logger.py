"""

Created on Oct 22, 2015
@author: wujz

"""

# -*- coding: utf-8 -*-
import logging
import traceback
import os

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET


class Logger:

    def __init__(self, filename, logger_name):
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.filename = filename
        self.fh = None
        self.ch = None

        try:
            if not os.path.exists(self.filename):
                fp = open(self.filename, 'w')
                fp.close()

            self.add_file_handler(filename, formatter)
            self.add_stream_handler(formatter)
        except Exception as e:
            raise e

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg, e):
        if isinstance(e, Exception):
            error_info = str(traceback.format_exc())
            msg += '\n' + error_info
        self.logger.error(msg)

    def add_file_handler(self, filename, formatter):
        self.fh = logging.FileHandler(filename)
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(formatter)
        self.logger.addHandler(self.fh)

    def add_stream_handler(self, formatter):
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)

    def close(self):
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.ch)
        self.fh.close()
        self.ch.close()
