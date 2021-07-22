#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: nols

import re

def vote(ip):
    test = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    if test.match(ip):
        return ip

