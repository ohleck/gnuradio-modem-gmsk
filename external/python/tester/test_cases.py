from .logger_utils import create_main_header, create_section, create_subsection

from time import sleep

from datetime import datetime

import hashlib
import os

import sys


class TestCase(object):
    """docstring for TestCase"""

    def __init__(self, test_number, description):
        super(TestCase, self).__init__()

        self.test_number = test_number

        self.create_logfile(self.test_number, description)

    def create_logfile(self, test_number, description):
        # ==============================================================
        # LOG FILE INITIALIZATION

        self.start_time = datetime.now()

        date_string = '{}_{}_{}'.format(self.start_time.day, self.start_time.month, self.start_time.year)
        time_string = '{}_{}_{}'.format(self.start_time.hour, self.start_time.minute, self.start_time.second)

        file_title = 'log/{}/test_cases/log_tc_{}_{}.txt'.format(date_string, test_number, time_string)
        os.makedirs(os.path.dirname(file_title), exist_ok=True)
        self.log_file = open(file_title, 'w+')

        info = create_main_header(description)
        self.add_to_log(info)

    def add_to_log(self, info):
        self.log_file.write(info)

if __name__ == '__main__':
    description = 'Some random test'
    tc = TestCase('1', description, local=True)
