#coding=utf-8
from appium import webdriver
import time
import re
import random
from BaseAdb import AndroidDebugBridge

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
x=raw_input(u'输入循环次数:')

def swipeLeft():
    width = driver.get_window_size()["width"]
    height = driver.get_window_size()["height"]
    x1 = int(width * 0.75)
    y1 = int(height * 0.5)
    x2 = int(width * 0.05)
    driver.swipe(x1, y1, x2, y1, 600)

def swiperandom():
    width = driver.get_window_size()["width"]
    height = driver.get_window_size()["height"]
    list_parmas=[0.05,0.75]
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

    print "----runnerPool------"
    print l_devices[i]

desired_caps = {
                'platformName': 'Android',
                'deviceName': l_devices[i]["devices"],
                'platformVersion': '7.0',
                'appPackage': 'com.bkjk.apollo.test',
                'appActivity': 'com.apollo.activity.AppLaucherActivity',
                'unicodeKeyboard': True, #此两行是为了解决字符输入不正确的问题
                'resetKeyboard': True    #运行完成后重置软键盘的状态　　
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
print driver
# lisst=driver.find_elements_by_xpath('//*')
# print lisst
# print "-------------------------------"
# aa=driver.current_activity
# print aa
print "================================="
#跳过导航页
time.sleep(4)
swipeLeft()
swipeLeft()
time.sleep(1)
# driver.find_elements_by_name('立即体验').click()
driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
ee=driver.find_element_by_id("com.bkjk.apollo.test:id/rl_im").is_enabled()
print ee
driver.find_element_by_id("com.bkjk.apollo.test:id/rl_im").click()

count = 0

while (count < int(x)):
# while True:
    try:
        # time.sleep(1)
        print '-------------start-------------------'
        print driver.current_activity
        result=driver.page_source
        print "--------------id all-----------------"
        id_result=re.findall('resource-id="(.*?)" instance=',result,re.S)
        #当前页面全部id
        for i in range(id_result.count('')):
            id_result.remove('')
        print id_result
        print "~~~~~~~~~~~~~~~choice id~~~~~~~~~~~~~~~~~~~~~~~~"

        bb = random.randint(1, len(id_result)-1)
        cc= id_result[bb]
        # print bb
        print cc
        print "~~~~~~~~~~~~~~~~~app is exist?~~~~~~~~~~~~~~~~~~~~~~"
        if desired_caps['appPackage'] in cc:
            print 'yes'
            pass
        elif 'android:id' in cc:
            print 'yet'
            pass
        else:
            print 'no'
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
            print driver
            time.sleep(4)
            swipeLeft()
            swipeLeft()
            time.sleep(1)
            # driver.find_elements_by_name('立即体验').click()
            driver.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
            continue

        print "~~~~~~~~~~~~~~~~~monkey~~~~~~~~~~~~~~~~~~~~~~"

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
        print 'Exception:',e
        continue
print "-----------end-------------"
print "count:",count



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

