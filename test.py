# import os.path
# from os import path
#
# my_path = "python-ios/bbc-my-news/S0/negative_oracle_state_ids.txt"
# if path.exists(my_path):
#     print("file_exists")
# else:
#     print("file not exists")

from appium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



class Explorer:
    def __init__(self):
        self.desiredCapabilities = {
              "platformName": "iOS",
              "platformVersion": "13.5",
              "deviceName": "Someone's iPhone",
              "udid": "auto",
              "xcodeOrgId": "87Z8B777X6",
              "xcodeSigningId": "iPhone Developer",
              "newCommandTimeout": 100000
        }

        d = webdriver.Remote('http://localhost:4723/wd/hub', self.desiredCapabilities)
        assert d is not None
        self.driver = d

if __name__ == "__main__":
    explorer = Explorer()

    #elem = explorer.driver.find_element_by_xpath("(//XCUIElementTypeStaticText[@name=\"1 undone task\"])[1]").click()
    elems = explorer.driver.find_elements_by_name("1 undone task")
    for elem in elems:
        elem.click()
#     elem = explorer.driver.find_element_by_id("com.contextlogic.wish:id/action_bar_item_icon")
#     elem.click()
#     try:
#         WebDriverWait(explorer.driver, 2).until(EC.presence_of_element_located((By.NAME, "See Suggested Topics")))
#     except:
#         print("widget exists assertion failed for ")
#     #WebDriverWait(explorer.driver, 10).until(EC.presence_of_element_located((By.ID, "com.contextlogic.wish:id/action_bar_item_icon")))
