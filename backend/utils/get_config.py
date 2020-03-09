#/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser
import sys
import os

def get_conf(section,confname):

    CONF_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = configparser.ConfigParser()
    config.read(os.path.join(CONF_DIR,'Journey.conf'))
    confname = config.get(section,confname)

    return confname