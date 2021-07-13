from appium import webdriver
import layout_tree as LayoutTree
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Explorer:
    def __init__(self):
        self.desiredCapabilities = {
          "platformName": "Android",
          "deviceName": "Pixel_4_API_30",
          "newCommandTimeout": 10000
        }

        d = webdriver.Remote('http://localhost:4723/wd/hub', self.desiredCapabilities)
        assert d is not None
        self.driver = d



    def check_text_exist_assertion(self, text, state_name_path):
        print(text)

    def check_text_invisible_assertion(self, text, state_name_path):
        print(text)

    def check_element_invisible_assertion(self, event):
        if event.exec_id_type == "accessibility-id":
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.ACCESSIBILITY_ID, event.exec_id_val)))
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


    def extract_state(self, state_name_path):
        layout = LayoutTree.LayoutTree(self.driver, state_name_path)
        curr_state = layout.extract_state()
        for element in curr_state.nodes:
            exec_identifier = ""
            if element.interactable:
                if 'content-desc' in element.attributes.keys():
                    element.add_data('content-desc', element.attributes['content-desc'])
                    element.add_exec_identifier('accessibility-id', element.attributes['content-desc'])
                    exec_identifier_val = element.attributes['content-desc']
                    exec_identifier = 'accessibility-id'
                if 'id' in element.attributes.keys():
                    element.add_data('id', element.attributes['id'])
                    element.add_exec_identifier('id', element.attributes['id'])
                    exec_identifier_val = element.attributes['id']
                    exec_identifier = 'id'
                if 'resource-id' in element.attributes.keys():
                    element.add_data('resource-id', element.attributes['resource-id'])
                    element.add_exec_identifier('resource-id', element.attributes['resource-id'])
                    exec_identifier_val = element.attributes['resource-id']
                    exec_identifier = 'resource-id'

                if 'text' in element.attributes.keys():
                    element.add_data('text', element.attributes['text'])

            # for interaction in element.interactions:
            #     if interaction == "click":
            #         curr_state.add_action(element.id, exec_identifier_val, interaction)

        return curr_state


    def execute_event(self, event):
        elem = None
        alreadyClicked = False
        print(event)
        if event.action == "oracle-text_exists":
            return
        elif event.action == "oracle-widget_exists":
            self.check_element_exists_assertion(event)
            return
        elif event.action == "oracle-element_invisible":
            self.check_element_invisible_assertion(event)
        elif event.action == "oracle-assert_equal":
            text_input = event.text_input
            attribute = text_input.split(" : ")[0]
            value = text_input.split(" : ")[1]
        elif event.action == "back":
            self.driver.back()
        else:
            if event.exec_id_type == "accessibility-id":
                time.sleep(6)
                print(event.exec_id_val)
                elem = self.driver.find_element_by_accessibility_id(event.exec_id_val)

            if event.exec_id_type == "xPath":
                time.sleep(3)
                elem = self.driver.find_element_by_xpath(event.exec_id_val[0])

            if event.exec_id_type == "resource-id":
                time.sleep(3)
                elem = self.driver.find_element_by_id(event.exec_id_val)

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
                elem.send_keys(event.text_input)
                self.driver.press_keycode(66)

            if not alreadyClicked:
                elem.click()




