import unittest
from lxml import etree as ET
import re
from appium import webdriver
import time
desired_caps = {
        "platformName": "iOS",
        "platformVersion": "13.4.1",
        "deviceName": "Someone's iPhone",
        "udid": "auto",
        "xcodeOrgId": "F9YGX7YPBF",
        "xcodeSigningId": "iPhone Developer",
        "bundleId": "com.foxnews.foxnews",
        "fullContextList":"true"
}

if __name__ == "__main__":
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    apps=driver.execute_script("mobile:activeAppInfo")
    #esired_caps["bundleId"]=apps["bundleId"]
    
    
    #findMinElement(337,642)
    print(apps)
    while True:
        context=driver.contexts
        print(context)
        time.sleep(10)