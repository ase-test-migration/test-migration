from appium import webdriver
import layout_tree as LayoutTree
import time
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



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
        # self.extract_state(state_name_path)
        print(text)
        # print(EC.text_to_be_present_in_element((By.XPATH, "/hierarchy/android.widget.FrameLayout"), text))

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


            if 'text' in element.attributes.keys():
                pass
                # element.ad
            # for interaction in element.interactions:
            #     if interaction == "click":
            #         curr_state.add_action(element.id, exec_identifier_val, interaction)

        return curr_state

    def execute_event(self, event):
        elem = None
        alreadyClicked = False
        print(event)
        if event.action == "oracle-text_exists" or event.action == "oracle-widget_exists":
            return
        if event.action == "oracle-assert_equal":
            text_input = event.text_input
            attribute = text_input.split(" : ")[0]
            value = text_input.split(" : ")[1]
        if event.action == "back":
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




if __name__ == "__main__":
    explorer = Explorer()

    # explorer.driver.scroll(10,100)
    # handle_one_size = explorer.driver.get_window_size()
    # print(handle_one_size)
    # #scroll_down
    # TouchAction(explorer.driver).long_press(x=handle_one_size['height']/2, y=handle_one_size['height']-1, duration=1000).move_to(x=handle_one_size['height']/2, y=1).release().perform()
    # #scroll_up
    # TouchAction(explorer.driver).long_press(x=handle_one_size['height']/2, y=200, duration=1000).move_to(x=handle_one_size['height']/2, y=handle_one_size['height']-1).release().perform()
    elem = explorer.driver.find_element_by_id("com.contextlogic.wish:id/action_bar_item_icon")
    elem.click()
    WebDriverWait(explorer.driver, 10).until(EC.presence_of_element_located((By.ID, "com.contextlogic.wish:id/browse_button")))
    WebDriverWait(explorer.driver, 10).until(EC.presence_of_element_located((By.ID, "com.contextlogic.wish:id/action_bar_item_icon")))