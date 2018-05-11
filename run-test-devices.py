#coding=utf-8
from appium import webdriver
import sys
import time
import re
import os
import random
import logging
from BaseAdb import AndroidDebugBridge
from BaseAndroidPhone import getPhoneInfo
from BaseDevicesInfo import devices_info
import LogcatAndroid
import subprocess
import threading
from get_package_pid import get_pid
from get_package_pid import kill_pid
from BaseAppiumServer import AppiumServer

#定义系统输出编码
reload(sys)
sys.setdefaultencoding('utf-8')

#定义PATH
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

FILE=os.getcwd()+'\\log\\'
now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
filename =now+u"运行log.txt"

#定义日志输出
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename = os.path.join(FILE,filename),
                filemode='w')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
logger = logging.getLogger()#fib
logger.setLevel(logging.INFO)#fib
console = logging.StreamHandler()
#console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(levelname)s: %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)#fib



num=raw_input(u'请输入MONKEY循环次数:')


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
        logging.info(e)
    return element

# appium_server=AppiumServer.start_server(devices_info())
# appium_server.start_server()


#多设备并行连接
def desired_caps():
    caps=[]
    print AndroidDebugBridge().attached_devices()
    for i in range(0,len(AndroidDebugBridge().attached_devices())):
        desired_caps = {}
        desired_caps['platformName']='Android'
        desired_caps['deviceName']= AndroidDebugBridge().attached_devices()[i]
        desired_caps['platformVersion']= getPhoneInfo(AndroidDebugBridge().attached_devices()[i])["release"]
        desired_caps['appPackage']= 'com.bkjk.apollo.test'
        desired_caps['appActivity']= 'com.apollo.activity.AppLaucherActivity'
        # desired_caps['app']=
        desired_caps['noReset'] = True    #不要在会话前重置应用状态
        desired_caps['fullReset'] = False   #通过卸载——而不是清空数据——来重置应用状态
        desired_caps['unicodeKeyboard']= True #此两行是为了解决字符输入不正确的问题
        desired_caps['resetKeyboard']= True    #运行完成后重置软键盘的状态　　
        caps.append(desired_caps)
        # driver = webdriver.Remote('http://localhost:'+str(4723+2*i)+'/wd/hub', caps[i])
    print caps
    return caps

tt=[]
for i in range(0,len(AndroidDebugBridge().attached_devices())):
    driver = webdriver.Remote('http://localhost:'+str(4723+2*i)+'/wd/hub', desired_caps()[i])

    t=threading.Thread(target=run_case())
    tt.append(t)



logging.info("----------------所有连接的设备--------------------")
logging.info(devices_info())

t = time.time()
#启动，drivers=driver()多次调用相当于重复启动----错误
# def driver2():
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
#     print driver
#     return driver




def run_case(dd):
    global dd
    # lisst=driver.find_elements_by_xpath('//*')#展示全部xpath路径
    # print lisst
    logging.info("-------------current_activity------------------")
    aa = dd.current_activity
    logging.info(aa)
    if '.AppGuideActivity' in aa:
        try:
            logging.info("===============导航页==================")
            # 跳过导航页
            dd.implicitly_wait(5)
            time.sleep(4)
            swipeLeft()
            swipeLeft()
            time.sleep(1)
            logging.info(
                'is enable?' + dd.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").is_enabled())
            dd.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
        except Exception as e:
            logging.info(e)
    else:
        pass
    count = 0
    error_count = 0
    while (count < int(num)):

        # while True:
        try:
            # time.sleep(1)
            logging.info('------------------current_activity---------------------')
            logging.info(driver.current_activity)
            if 'apollo' not in dd.current_activity:
                dd.press_keycode(4)
                time.sleep(0.2)
                if 'apollo' not in dd.current_activity:
                    logging.info('not find APP,ready to restart......')
                    dd = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps())
                    if '.AppGuideActivity' in dd.current_activity:
                        try:
                            time.sleep(4)
                            swipeLeft()
                            swipeLeft()
                            dd.implicitly_wait(6)
                            dd.find_element_by_id("com.bkjk.apollo.test:id/btn_enter_home").click()
                        except Exception as e:
                            logging.info(e)
                    else:
                        pass
                else:
                    pass
            else:
                pass
            result = dd.page_source
            logging.info("------------------------id all--------------------------")
            id_result = re.findall('resource-id="(.*?)" instance=', result, re.S)
            # 当前页面全部id
            for n in range(id_result.count('')):
                id_result.remove('')
            logging.info(id_result)
            logging.info("------------------------choice id------------------------")

            bb = random.randint(1, len(id_result) - 1)
            cc = id_result[bb]
            # print bb
            logging.info(cc)
            logging.info("------------------------app is exist?------------------------")
            if desired_caps()['appPackage'] in cc:
                logging.info('yes')
                pass
            elif 'android:id' in cc:
                logging.info('yet')
                pass
            else:
                logging.info('no')
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
                        logging.info(e)
                else:
                    pass
                continue

            logging.info("------------------------monkey--------------------------")  # 慢的问题？
            enable = driver.find_element_by_id(cc).is_enabled()
            logging.info('isenable:' + str(enable))
            rate = random.randint(1, 10)  # 调整动作几率
            if rate == 1:
                # print activity + ' Scroll left'
                swiperandom()
                logging.info('swipe:' + str(swiperandom()))
            elif rate == 10:
                # print activity + ' Key Back'
                driver.press_keycode(4)
                logging.info('点击 Back')
            else:
                # print activity + ' Scroll Up'
                if 'android:id' in cc:
                    driver.press_keycode(4)
                    logging.info('点击 Back')
                else:
                    driver.find_element_by_id(cc).click()
                    logging.info('点击:' + str(cc))

            count = count + 1

            logging.info("执行: 第 " + str(count) + ' 次')
        except Exception as e:
            error_count = error_count + 1
            logging.info('Error ' + str(e))
            continue
    logging.info("====================end========================")
    logging.info("count:" + str(count))
    logging.info('Error Message:' + str(error_count))
    logging.info('%.3f' % (time.time() - t) + "秒")




#定义logcat输出
FILE2 =FILE+ 'logcat'+now + '.log'
with open(FILE2, 'w') as logcat_file:
        # os.popen(LogcatAndroid.logcat_filein(desired_caps()['appPackage'], FILE2))
    Poplog= subprocess.Popen(LogcatAndroid.logcat_filein(desired_caps()['appPackage']),shell=True,stdout=logcat_file,stderr=subprocess.PIPE)


if __name__ == '__main__':

    print devices_info()
    # a = AppiumServer(devices_info())
    # a.start_server()
    run_case()
    time.sleep(5)
    kill_pid('adb.exe')
    Poplog.terminate()



