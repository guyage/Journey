#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess

def exec_cmd(cmd):
    res = subprocess.Popen(args=cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return res.stdout.read()