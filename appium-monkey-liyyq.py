#coding=utf-8
from appium import webdriver
import time
import re
import os
import random
from BaseAdb import AndroidDebugBridge
from BaseAndroidPhone import getPhoneInfo
from LogcatAndroid import logcat

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# x=raw_input(u'请输入MONKEY循环次数:')

def swipeLeft():
    drivers=driver()
    print '111'
    width = drivers.get_window_size()["width"]
    print '222'
    height = drivers.get_window_size()["height"]
    x1 = int(width * 0.75)
    y1 = int(height * 0.5)
    x2 = int(width * 0.25)
    driver().swipe(x1, y1, x2, y1, 600)
    print '333'

def swiperandom():
    drivers=driver()
    width = drivers.get_window_size()["width"]
    height = drivers.get_window_size()["height"]
    list_parmas=[0.25,0.75]
    x1 = int(width * list_parmas[random.randint(0,1)])
    y1 = int(height * list_parmas[random.randint(0,1)])
    x2 = int(width * list_parmas[random.randint(0,1)])
    y2 = int(height * list_parmas[random.randint(0,1)])
    driver().swipe(x1, y1, x2, y2, 300)
    return [(x1, y1), (x2, y2)]

def find_element_by_id_no_except(id):
    element = None
    try :
        element = driver().find_element_by_id(id)
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
    desired_caps['unicodeKeyboard']= True #此两行是为了解决字符输入不正确的问题
    desired_caps['resetKeyboard']= True    #运行完成后重置软键盘的状态　　
    return desired_caps

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
#启动，drivers=driver()多次调用相当于重复启动----错误
# def driver():
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
#     print driver
#     return driver

def test_case():
    # lisst=driver.find_elements_by_xpath('//*')
    # print lisst
    # print "-------------------------------"
    # aa=driver.current_activity
    # print aa
    try:
        print "================================="
        #跳过导航页
        driver.implicitly_wait(5)
        time.sleep(4)
        print 'sleep444444'
        swipeLeft()
        swipeLeft()
        time.sleep(1)
        # driver.find_elements_by_name('立即体验').click()
        print 'is enable?',driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").is_enabled()
        driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
    except Exception as e:
        print e
    count = 0
    error_count=0
    while (count < int(50)):
    # while True:
        try:
            # time.sleep(1)
            print '-------------start-------------------'
            print driver.current_activity
            result=driver.page_source
            print "--------------id all-----------------"
            id_result=re.findall('resource-id="(.*?)" instance=',result,re.S)
            #当前页面全部id
            for n in range(id_result.count('')):
                id_result.remove('')
            print id_result
            print "~~~~~~~~~~~~~~~choice id~~~~~~~~~~~~~~~~~~~~~~~~"

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
                driver2 = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
                time.sleep(4)
                swipeLeft()
                swipeLeft()
                time.sleep(1)
                # driver.find_elements_by_name('立即体验').click()
                driver2.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
                continue

            print "~~~~~~~~~~~~~~~~~monkey~~~~~~~~~~~~~~~~~~~~~~"
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
    print "-----------end-------------"
    print "count:",count
    print 'message:',error_count

if __name__ == '__main__':
    # print desired_caps()['appPackage']
    # devices_info()
    print "-----------所有连接的设备-----------"
    print devices_info()

    test_case()

    # else:
    #     btn_list = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
    #     if (len(btn_list) > 0):
    #         index = random.randint(0, len(btn_list) - 1)
    #         print activity + ' Click Button index = %d' % (index,)
    #         btn_list[index].click()

# driver.find_element_by_id("com.baidu.searchbox:id/baidu_searchbox").click()
# driver.find_element_by_id("com.baidu.searchbox:id/SearchTextInput").clear()
# driver.find_element_by_id("com.baidu.searchbox:id/SearchTextInput").send_keys('appium测试')
#
# driver.find_element_by_id("float_search_or_cancel").click()
# driver.find_element_by_id("floating_action_button").click()

