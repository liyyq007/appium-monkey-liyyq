#!/usr/bin/env python
#coding:utf-8

import os
import sys

def logcat(packageName):
    cmd = 'adb shell "logcat | grep --color=always -E \"%s\" "'% packageName
    os.system(cmd)
    print os.system(cmd)

if __name__ == '__main__':
    logcat('com.bkjk.apollo.test')


