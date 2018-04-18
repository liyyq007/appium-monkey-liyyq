import os
import shlex

def get_pid(packageName):
    try:
        p2=os.popen('adb shell ps | findstr %s' % packageName )
        args = shlex.split(p2)
        return args[1]
    except Exception as e:
        print e



if __name__ == '__main__':
    print get_pid('com.bkjk.apollo.test')