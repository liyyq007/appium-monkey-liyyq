import os
import shlex
import psutil
from BaseAdb import AndroidDebugBridge

def get_pid(n,packageName):
    try:
        p2=os.popen('adb -s %s shell ps | findstr %s' % (AndroidDebugBridge().attached_devices()[int(n)-1],packageName))
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
        # os.kill(i,9)
        os.popen('taskkill.exe -F /pid:'+str(i))


if __name__ == '__main__':
    print get_pid(2,'com.bkjk.apollo.test')
    # print get_pid('adb.exe')
    # print get_namepid('adb.exe')
    # kill_pid('adb.exe')
    # print p
