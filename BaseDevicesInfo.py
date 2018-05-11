#coding=utf-8
from BaseAdb import AndroidDebugBridge
import random

def devices_info():
    try:
        devicess = AndroidDebugBridge().attached_devices()
        print devicess
        if len(devicess) > 0:
            l_devices = []
            for dev in devicess:
                app = {}
                app["devices"] = dev
                app["port"] = str(random.randint(4700, 4900))
                app["bport"] = str(random.randint(4700, 4900))
                app["systemPort"] = str(random.randint(4700, 4900))
                l_devices.append(app)
                # print l_devices
            return l_devices
            # appium_server = AppiumServer.start_server(devices_info())
            # appium_server.start_server()
        # for i in range(0, len(l_devices)):
        #
        #     pass
        # return l_devices[i]
    except Exception as e:
        print u'设备连接异常,请检查设备连接',e