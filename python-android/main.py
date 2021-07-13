import json
from sys import argv

import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

import layout_tree

class StateExtractor:

    def __init__(self, metadataPath):
        with open(metadataPath) as f:
            metadata = json.load(f)

        desiredCapabilities = metadata["desiredCapabilities"]
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desiredCapabilities)
        assert driver != None

        self.driver = driver
        self.tests = metadata["tests"]


    def check_for_negative_oracles(self, negative_oracles, state_name_path):
        print("checking for negative oracle")
        base = state_name_path.split("/")[0]
        negative_oracles_state_ids = []
        for negative_oracle in negative_oracles:
            new_state_name_path = base + "/S" + str(negative_oracle["id"])
            event = negative_oracle["event"]
            elem = None
            if event["type"] == "accessibilityId":
                time.sleep(15)
                try:
                    elem = self.driver.find_element_by_accessibility_id(event["tag"])
                except:
                    pass
            if event["type"] == "xPath":
                time.sleep(15)
                try:
                    elem = self.driver.find_element_by_xpath(event["tag"])
                except:
                    pass
            if event["type"] == "id":
                time.sleep(15)
                try:
                    elem = self.driver.find_element_by_id(event["tag"])
                except:
                    pass

            if elem is not None:
                print("negative oracle found")
                negative_oracles_state_ids.append(negative_oracle["id"])
                self.createDir(new_state_name_path)
                layoutTree = layout_tree.LayoutTree(self.driver, new_state_name_path)
                pathToElementImage, bounds, textual_info = layoutTree.printTree(elem.rect)
                self.save_step(new_state_name_path, textual_info, pathToElementImage, bounds, negative_oracle["event"], [])

        return negative_oracles_state_ids

    def execEvent(self, event, stateNamePath, negative_oracles):
        elem = None
        alreadyClicked=False
        negative_oracles_state_ids = []
        if len(negative_oracles)!=0:
            negative_oracles_state_ids = self.check_for_negative_oracles(negative_oracles, stateNamePath)

        if event["event"] == "oracle" and (event["oracle-type"] == "text_exists" or event["oracle-type"] == "text_invisible") :
            return "", "", event["input"], []
        elif event["event"] == "oracle" and event["oracle-type"] == "element_invisible":
            return "", "", "", []
        elif event["event"] == "back":
            layoutTree = layout_tree.LayoutTree(self.driver, stateNamePath)
            layoutTree.printTree()
            self.driver.back()
            return "", "", "", []
        else:
            if event["type"] == "accessibilityId":
                print(event)
                # Instead of this you should be fatching the state.
                time.sleep(30)
                elem = self.driver.find_element_by_accessibility_id(event["tag"])

            if event["type"] == "xPath":
                # Instead of this you should be fatching the state.
                time.sleep(30)
                elem = self.driver.find_element_by_xpath(event["tag"])

            if event["type"] == "id":
                # Instead of this you should be fatching the state.
                time.sleep(30)
                elem = self.driver.find_element_by_id(event["tag"])

            layoutTree = layout_tree.LayoutTree(self.driver, stateNamePath)

            if event["type"] == "coordinate":
                # Instead of this you should be fatching the state.
                time.sleep(5)
                pathToElementImage, bounds=layoutTree.findMinElement(event["x"],event["y"])
                TouchAction(self.driver).tap(x=event["x"], y=event["y"]).perform()
                alreadyClicked=True
                layoutTree.printTree()
                #elem= self.driver.find_element_by_xpath
                return pathToElementImage, bounds

            if event["event"] == "send_keys":
                time.sleep(2)
                pathToElementImage, bounds, textual_info = layoutTree.printTree(elem.rect)
                elem.click()
                alreadyClicked=True
                time.sleep(1)
                elem.send_keys(event["input"])
                

            if event["event"] == "send_keys_enter":
                time.sleep(2)
                pathToElementImage, bounds, textual_info = layoutTree.printTree(elem.rect)
                elem.click()
                alreadyClicked=True
                time.sleep(1)
                elem.clear()
                elem.send_keys(event["input"])
                self.driver.press_keycode(66)
                # self.driver.press_keycode(66)


            if elem == None:
                print("ELEMENT NOT FOUND!: "+event)
                return

            # Save element info to metadata
            if event["event"] != "send_keys" and event["event"] != "send_keys_enter":
                pathToElementImage, bounds, textual_info = layoutTree.printTree(elem.rect)

            if event["event"]=="oracle":
               return pathToElementImage, bounds, textual_info, negative_oracles_state_ids

            if not alreadyClicked:
                elem.click()
            return pathToElementImage, bounds, textual_info, negative_oracles_state_ids

    def check_for_negative_oracle_existance(self, events):
        negative_oracles = []
        has_negative_oracle = False
        for index, event in enumerate(events):
            if event["event"] == "oracle":
                if event["oracle-type"] == "element_invisible":
                    print("found!")
                    negative_oracle = {
                        "id": index,
                        "event": event
                    }
                    negative_oracles.append(negative_oracle)
        if len(negative_oracles)>0:
            has_negative_oracle = True
            print("negative oracle exists")
        else:
            print("negative oracle does not exist")
        return has_negative_oracle, negative_oracles

    def save_step(self, stateNamePath, textual_info, pathToElementImage, bounds, event, negative_oracles_state_ids):
        textual_info = "{ " + textual_info + " }"
        with open("{}/event_metadata.txt".format(stateNamePath), "w") as f:
            f.write("pathToElementImageCrop: {};\n".format(pathToElementImage))
            f.write("coords: {};\n".format(bounds))
            f.write("text_identifier: {};\n".format(textual_info))
            f.write("event: {};\n".format(event["event"]))
            if event["event"] == "send_keys" or event["event"] == "send_keys_enter":
                f.write("input: {};\n".format(event["input"]))
            if event["event"] == "oracle":
                f.write("oracle-type: {};\n".format(event["oracle-type"]))
                if event["oracle-type"] == "text_exists" or event["oracle-type"] == "text_invisible":
                    f.write("input: {};\n".format(event["input"]))
                if event["oracle-type"] == "assert_equal":
                    print(event["attribute"])
                    f.write("attribute: {};\n".format(event["attribute"]))
                    f.write("value: {};\n".format(event["value"]))
        if len(negative_oracles_state_ids)>0:
            with open("{}/negative_oracle_state_ids.txt".format(stateNamePath), "w") as negative_oracles_file:
                for id in negative_oracles_state_ids:
                    negative_oracles_file.write(str(id)+"\n")

    def runTest(self, testName, events):
        self.createDir(testName)
        has_negative_oracles, negative_oracles = self.check_for_negative_oracle_existance(events)
        print("negative oracles:")
        for element in negative_oracles:
            print(element["id"])
        i = 0
        for event in events:
            stateNamePath = "{}/S{}".format(testName, i)
            self.createDir(stateNamePath)
            if event["event"]!="oracle" or event["oracle-type"]!="element_invisible":
                pathToElementImage, bounds, textual_info, negative_oracles_state_ids = self.execEvent(event, stateNamePath, negative_oracles)
                print(negative_oracles_state_ids)
                remove_list = []
                for element in negative_oracles:
                    print(element["id"])
                    if element["id"] in negative_oracles_state_ids:
                        remove_list.append(element)
                negative_oracles = [x for x in negative_oracles if x not in remove_list]
                self.save_step(stateNamePath, textual_info, pathToElementImage, bounds, event, negative_oracles_state_ids)
            i += 1


    def createDir(self, name):
        import os
        try:
            os.rmdir(name)
            
        except:
            print("{} Not exists.".format(name))
            pass

        try:
            os.mkdir(name)
        except:
            print("{} failed!.".format(name))
            pass

    def run(self):
        for test in self.tests:
            print("Running test: ", test["name"])
            self.runTest(test["name"], test["events"])   

if __name__ == "__main__":
    start = time.time()
    s = StateExtractor(argv[1])
    s.run()
    end = time.time()
    print("Android extraction running time: " + str(end - start) + " seconds")
