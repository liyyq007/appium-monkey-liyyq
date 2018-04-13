#coding=utf-8
from appium import webdriver
import time
import re
import os
import random
from BaseAdb import AndroidDebugBridge
from BaseAndroidPhone import getPhoneInfo
import subprocess

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# x=raw_input(u'请输入MONKEY循环次数:')

def swipeLeft():
    width = driver.get_window_size()["width"]
    height = driver.get_window_size()["height"]
    x1 = int(width * 0.75)
    y1 = int(height * 0.5)
    x2 = int(width * 0.25)
    driver.swipe(x1, y1, x2, y1, 600)

def swiperandom():
    width = driver.get_window_size()["width"]
    height = driver.get_window_size()["height"]
    list_parmas=[0.25,0.75]
    x1 = int(width * list_parmas[random.randint(0,1)])
    y1 = int(height * list_parmas[random.randint(0,1)])
    x2 = int(width * list_parmas[random.randint(0,1)])
    y2 = int(height * list_parmas[random.randint(0,1)])
    driver.swipe(x1, y1, x2, y2, 300)
    return [(x1, y1), (x2, y2)]

def find_element_by_id_no_except(id):
    element = None
    try :
        element = driver.find_element_by_id(id)
    except Exception,e:
        print Exception, ':', e
    return element

def devices_info():
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

    for i in range(0, len(l_devices)):
        pass
    return l_devices[i]

def desired_caps():
    desired_caps = {}
    desired_caps['platformName']='Android'
    desired_caps['deviceName']= devices_info()["devices"]
    desired_caps['platformVersion']= getPhoneInfo(devices_info()["devices"])["release"]
    desired_caps['appPackage']= 'com.bkjk.apollo.test'
    desired_caps['appActivity']= 'com.apollo.activity.AppLaucherActivity'
    # desired_caps['app']=
    desired_caps['noReset'] = True    #不要在会话前重置应用状态
    desired_caps['fullReset'] = False   #通过卸载——而不是清空数据——来重置应用状态
    desired_caps['unicodeKeyboard']= True #此两行是为了解决字符输入不正确的问题
    desired_caps['resetKeyboard']= True    #运行完成后重置软键盘的状态　　
    return desired_caps

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())

#启动，drivers=driver()多次调用相当于重复启动----错误
# def driver2():
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
#     print driver
#     return driver

def test_case():
    global driver
    # lisst=driver.find_elements_by_xpath('//*')#展示全部xpath路径
    # print lisst
    print "-------------current_activity------------------"
    aa=driver.current_activity
    print aa
    if '.AppGuideActivity' in aa:
        try:
            print "===============导航页=================="
            #跳过导航页
            driver.implicitly_wait(5)
            time.sleep(4)
            swipeLeft()
            swipeLeft()
            time.sleep(1)
            print 'is enable?',driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").is_enabled()
            driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
        except Exception as e:
            print e
    else:
        pass
    count = 0
    error_count=0
    while (count < int(50)):

    # while True:
        try:
            # time.sleep(1)
            print '------------------current_activity---------------------'
            print driver.current_activity
            result=driver.page_source
            print "----------------------id all--------------------------"
            id_result=re.findall('resource-id="(.*?)" instance=',result,re.S)
            #当前页面全部id
            for n in range(id_result.count('')):
                id_result.remove('')
            print id_result
            print "~~~~~~~~~~~~~~~~~~~choice id~~~~~~~~~~~~~~~~~~~~~~~~"

            bb = random.randint(1, len(id_result)-1)
            cc= id_result[bb]
            # print bb
            print cc
            print "~~~~~~~~~~~~~~~~~app is exist?~~~~~~~~~~~~~~~~~~~~~~"
            if desired_caps()['appPackage'] in cc:
                print 'yes'
                pass
            elif 'android:id' in cc:
                print 'yet'
                pass
            else:
                print 'no'
                driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
                '''这会有问题-------给变量取的这个名字，可能会冲突，它是函数外部的变量，因为全局变量driver的值被修改
                -----在函数内加global driver，内部作用域的想要修改外部作用域的变量，就要使用global关键字'''
                if '.AppGuideActivity' in driver.current_activity:
                     try:
                        time.sleep(4)
                        swipeLeft()
                        swipeLeft()
                        driver.implicitly_wait(6)
                        driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
                     except Exception as e:
                        print e
                else:
                    pass
                continue

            print "~~~~~~~~~~~~~~~~~~~~~~~monkey~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            ee = driver.find_element_by_id(cc).is_enabled()
            print 'isenable:', ee
            rate = random.randint(1,10)
            if rate==1:
                # print activity + ' Scroll left'
                swiperandom()
                print 'swipe:',swiperandom()
            elif rate==2:
                # print activity + ' Key Back'
                driver.press_keycode(4)
                print 'Key Back'
            else:
                # print activity + ' Scroll Up'
                if 'android:id' in cc:
                    swiperandom()
                    print 'swipe:', swiperandom()
                else:
                    driver.find_element_by_id(cc).click()
                    print 'click:',cc

            count = count + 1

            print "count:",count
        except Exception as e:
            error_count=error_count + 1
            print 'Exception:',e
            continue
    print "====================end========================"
    print "count:",count
    print 'message:',error_count

if __name__ == '__main__':
    # print desired_caps()['appPackage']
    print "----------------所有连接的设备--------------------"
    print devices_info()
    Poplog = subprocess.Popen('adb shell "logcat | grep --color=always -E \"%s\" "'% desired_caps()['appPackage'])
    test_case()
    Poplog.terminate()
