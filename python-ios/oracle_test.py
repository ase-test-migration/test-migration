from builtins import AssertionError

from appium import webdriver
import layout_tree as LayoutTree
import time
import unittest
import node
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

    def extract_state(self, state_name_path):
        layout = LayoutTree.LayoutTree(self.driver, state_name_path)
        curr_state = layout.extract_state()

        for element in curr_state.nodes:
                if 'accessibility-id' in element.attributes.keys():
                    element.add_data('content-desc', element.attributes['content-desc'])
                    element.add_exec_identifier('accessibility-id', element.attributes['content-desc'])
                    exec_identifier_val = element.attributes['content-desc']
                    exec_identifier = 'accessibility-id'
                if 'name' in element.attributes.keys():
                    element.add_data('name', element.attributes['name'])
                    element.add_exec_identifier('name', element.attributes['name'])
                    exec_identifier = 'name'
                    print(element.attributes['name'])
                if 'label' in element.attributes.keys():
                    element.add_data('label', element.attributes['label'])
                    print(element.attributes['label'])
                if 'value' in element.attributes.keys():
                    element.add_data('value', element.attributes['value'])
                    print(element.attributes['value'])


        return curr_state


    def check_text_exist_assertion(self, text, state_name_path):
        # self.extract_state(state_name_path)
        print(text)
        # print(EC.text_to_be_present_in_element((By.XPATH, "/hierarchy/android.widget.FrameLayout"), text))

    def execute_event(self, event):
        elem = None
        alreadyClicked = False
        if event.action == "oracle-text_exists" or event.action == "oracle-widget_exists":
            return
        if event.action == "back":
            self.driver.back()
        else:
            if event.exec_id_type == "accessibility-id":
                print(event)
                time.sleep(5)
                elem = self.driver.find_element_by_accessibility_id(event.exec_id_val)

            if event.exec_id_type == "xPath":
                time.sleep(3)
                elem = self.driver.find_element_by_xpath(event.exec_id_val)

            if event.exec_id_type == "resource-id":
                time.sleep(3)
                elem = self.driver.find_element_by_id(event.exec_id_val)

            if event.exec_id_type == "name":
                time.sleep(3)
                elem = self.driver.find_element_by_name(event.exec_id_val)

            if event.action == "send_keys":
                time.sleep(2)
                elem.click()
                alreadyClicked = True
                time.sleep(1)
                elem.send_keys(event.text_input)

            if event.action == "send_keys_enter":
                time.sleep(2)
                elem.click()
                alreadyClicked = True
                time.sleep(1)
                elem.send_keys(event.text_input + '\n')
                # elem.send_keys(Keys.ENTER)


            if not alreadyClicked:
                elem.click()


if __name__ == "__main__":
    # explorer = Explorer()
    x=2
    # time.sleep(5)
    # print(explorer.driver.find_element_by_name('Popular').get_attribute("value"))
    # print(explorer.driver.find_element_by_name('Brands').get_attribute("value"))
    try:
        assert x==2, "x should be 2"
        assert x==3, "x shouldn't be 3"
    except AssertionError as error:
        print(error)
