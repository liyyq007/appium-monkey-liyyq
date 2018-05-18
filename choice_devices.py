#coding=utf-8
from BaseAdb import AndroidDebugBridge
import random

def devices_info():
    try:
        devicess = AndroidDebugBridge().attached_devices()
        if len(devicess) > 0:
            l_devices = []
            for dev in devicess:
                app = {}
                app["devices"] = dev
                app["port"] = str(random.randint(4700, 4900))
                app["bport"] = str(random.randint(4700, 4900))
                app["systemPort"] = str(random.randint(4700, 4900))
                l_devices.append(app)
            # return l_devices#返回全部设备
        # for i in range(0, len(l_devices)):
        #     pass
        return l_devices
    except Exception as e:
        print u'设备连接异常,请检查设备连接',e

def choice_devices():
    n=int(raw_input('devices列表：\n%s \n请选择设备(1,2,3,4....):'%AndroidDebugBridge().attached_devices()))-1
    return n

if __name__ == '__main__':
#     # c='sss'
#     # print a(c)
    choice_devices()