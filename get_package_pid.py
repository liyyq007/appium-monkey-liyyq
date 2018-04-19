import os
import shlex
import psutil

def get_pid(packageName):
    try:
        p2=os.popen('adb shell ps | findstr %s' % packageName )
        args = shlex.split(p2)
        return args[1]
    except Exception as e:
        print e


def get_namepid(name):
    idlist=[]
    pid=psutil.pids()
    for id in pid:
        p = psutil.Process(id)
        if name in p.name():
            idlist.append(id)
        else:
            pass
    return idlist

def kill_pid(name):
    for i in get_namepid(name):
        os.kill(i,9)

if __name__ == '__main__':
    # print get_pid('com.bkjk.apollo.test')
    # print get_pid('adb.exe')
    print get_namepid('adb.exe')
    kill_pid('adb.exe')
    # print p
