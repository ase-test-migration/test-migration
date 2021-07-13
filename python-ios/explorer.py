import time
from builtins import AssertionError

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import layout_tree as LayoutTree


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

    def check_element_invisible_assertion(self, event):
        if event.exec_id_type == "accessibility-id":
            try:
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ACCESSIBILITY_ID, event.exec_id_val)))
            except:
                print("Element invisible assertion failed.")

        if event.exec_id_type == "xPath":
            try:
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, event.exec_id_val)))
            except:
                print("Element invisible assertion failed.")

        if event.exec_id_type == "resource-id":
            try:
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, event.exec_id_val)))
            except:
                print("Element invisible assertion failed.")

        if event.exec_id_type == "name":
            try:
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.NAME, event.exec_id_val)))
            except:
                print("Element invisible assertion failed.")

    def check_text_invisible_assertion(self, text, state_name_path):
        print(text)

    def check_element_exists_assertion(self, event):
        if event.exec_id_type == "accessibility-id":
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ACCESSIBILITY_ID, event.exec_id_val)))
            except:
                print("Widget exists assertion failed.")

        if event.exec_id_type == "xPath":
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, event.exec_id_val)))
            except:
                print("Widget exists assertion failed.")

        if event.exec_id_type == "resource-id":
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, event.exec_id_val)))
            except:
                print("Widget exists assertion failed.")

        if event.exec_id_type == "name":
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, event.exec_id_val)))
            except:
                print("Widget exists assertion failed.")

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
                print("in exec event")
                time.sleep(3)
                print(event.exec_id_val)
                elem = self.driver.find_element_by_xpath(event.exec_id_val)
                print("done with finding")

            if event.exec_id_type == "resource-id":
                time.sleep(3)
                elem = self.driver.find_element_by_id(event.exec_id_val)

            if event.exec_id_type == "name":
                time.sleep(3)
                elems = self.driver.find_elements_by_name(event.exec_id_val)
                for elem in elems:
                    try:
                        elem.click()
                        alreadyClicked = True
                    except:
                        pass

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
                #elem.send_keys(Keys.ENTER)

            if event.action == "oracl-assert_equal":
                text_input = event.text_input
                if text_input == "not_mappable":
                    return
                attribute = text_input.split(" : ")[0]
                value = text_input.split(" : ")[1]
                if attribute != "checked" and attribute != "selected":
                    try:
                        assert attribute==value, "the value for "+attribute+" should be "+value
                    except AssertionError as error:
                        print(error)
                if attribute == "checked" and value == True:
                    result = (element.get_attribute("value")==1) or (element.get_attribute("value")=="selected") or (element.get_attribute("value")=="checked")
                    try:
                        assert result==True, "assertion result should be True"
                    except AssertionError as error:
                        print(error)
                if attribute == "selected" and value == True:
                    result = (element.get_attribute("value")==1) or (element.get_attribute("value")=="selected") or (element.get_attribute("value")=="checked")
                    try:
                        assert result==True, "assertion result should be True"
                    except AssertionError as error:
                        print(error)
            if not alreadyClicked:
                print("in click")
                elem.click()


if __name__ == "__main__":
    explorer = Explorer()
    explorer.extract_state("m")
    time.sleep(5)
    element = explorer.driver.find_element_by_name("Reviews")
    element.click()