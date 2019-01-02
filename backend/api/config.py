#/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser
import sys
import os
import random, string

def get_conf(section,confname):

    CONF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = configparser.ConfigParser()
    config.read(os.path.join(CONF_DIR,'sql_platform.conf'))
    confname = config.get(section,confname)

    return confname

def random_str(randomlength=10):
        a = list(string.ascii_letters)
        random.shuffle(a)
        return ''.join(a[:randomlength])


