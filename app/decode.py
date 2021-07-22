#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: nols

import urllib.parse
import base64

def urldecode(argv):
    urldecode = urllib.parse.unquote(argv)
    return urldecode


def base64decode(argv):

    base64decode = str(base64.b64decode(argv), "utf-8")
    return base64decode

def Unicode(argv):
    Unicodedecode=argv.encode('utf-8').decode('unicode_escape')
    return Unicodedecode


def str2byte(s):
    base='0123456789ABCDEF'
    i=0
    s = s.upper()
    s1=''
    while i < len(s):
        c1=s[i]
        c2=s[i+1]
        i+=2
        b1=base.find(c1)
        b2=base.find(c2)
        if b1 == -1 or b2 == -1:
            return None
        s1+=chr((b1 << 4)+b2)
    return s1

