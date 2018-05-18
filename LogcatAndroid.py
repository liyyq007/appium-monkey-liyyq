#!/usr/bin/env python
# coding:utf-8

import os
import sys
import subprocess

from get_package_pid import get_pid

def logcat_filein(n,packageName):
    # logcat_file=open('log1.txt','w')
    cmd = 'adb shell "logcat |grep --color=always -E \"%s\""  '% get_pid(n,packageName)
    # cmd = 'adb logcat '
    # cmd='adb shell "logcat | grep --color=always -E \"com.bkjk.apollo.test\"" -f D:/test/appium-monkey-liyyq/log.txt -s "TAG：*"'
    # os.popen(cmd)
    # print os.system(cmd)
    return cmd

def logcat(packageName):
    # logcat_file=open('log1.txt','w')
    cmd = 'adb shell "logcat | grep --color=always -E \"%s\""'% packageName
    # cmd='adb shell "logcat | grep --color=always -E \"com.bkjk.apollo.test\"" -f D:/test/appium-monkey-liyyq/log.txt -s "TAG：*"'
    # os.system(cmd)
    # print os.system(cmd)
    return cmd

# pp=subprocess.Popen('adb shell logcat >> 111.txt')
# pp.terminate()
# pp=subprocess.Popen('adb  logcat -v time')
# pp.terminate()
# p=subprocess.Popen(logcat_filein('com.bkjk.apollo.test','111.txt'))
if __name__ == '__main__':
    # p=subprocess.Popen(logcat_filein('com.bkjk.apollo.test','112.txt'))
    # p = subprocess.Popen('adb shell logcat >> 111.txt')
    print logcat_filein('com.bkjk.apollo.test')
    # LogcatAndroid.logcat_filein(desired_caps()['appPackage']), shell = True, stdout = logcat_file, stderr = subprocess.PIPE)

    # p.terminate()


    # print logcat('com.bkjk.apollo.test')
    # print '111111111111111111111111111111111111111111111111111111111111111111111111111111111111'


