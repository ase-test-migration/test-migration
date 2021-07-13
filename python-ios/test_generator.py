from sys import argv
import re
import json
import os

class TestGenerator:
    def __init__(self, test_file_path, test_name):
        self.test_file_path = test_file_path
        self.current_step = 0
        self.device_capabilities = {}
        self.document = {"desiredCapabilities": self.device_capabilities}
        self.test = {"name": test_name}
        self.events = []
        print(test_name)
        self.test_name = test_name.split("-")[1]
        self.app_name=test_name.split("-")[0]

    def add_step(self, event):
        new_event = {}
        print(event)
        if event.action == "oracle-text_exists":
            new_event["event"] = "oracle"
            new_event["oracle-type"] = "text_exists"
            new_event["input"] = event.text_input
        elif event.action == "back":
            new_event["event"] = "back"
        elif event.action == "oracle-text_invisible":
            new_event["event"] = "oracle"
            new_event["oracle-type"] = "text_invisible"
            new_event["input"] = event.text_input
        elif event.action == "oracle-assert_equal":
            new_event["event"] = "oracle"
            new_event["oracle-type"] = "assert_equal"
            text_input = event.text_input
            new_event["attribute"] = text_input.split(":")[0]
            new_event["value"] = text_input.split(":")[1]
            new_event["type"] = "accessibilityId"
            new_event["tag"] = event.exec_id_val
        else:
            if event.action == "oracle-widget_exists":
                new_event["event"] = "oracle"
                new_event["oracle-type"] = "widget_exists"

            if event.action == "oracle-element_invisible":
                new_event["event"] = "oracle"
                new_event["oracle-type"] = "element_invisible"

            if event.exec_id_type == "accessibility_id":
                new_event["type"] = "accessibilityId"
                new_event["tag"] =  event.exec_id_val

            if event.exec_id_type == "xPath":
                new_event["type"] = "xPath"
                new_event["tag"] = event.exec_id_val

            if event.exec_id_type == "resource-id":
                new_event["type"] = "xPath"
                new_event["tag"] = event.exec_id_val

            if event.exec_id_type == "name":
                new_event["type"] = "name"
                new_event["tag"] = event.exec_id_val

            new_event["event"] = event.action
            if event.action == "send_keys":
                new_event["input"] = event.text_input

            if event.action == "send_keys_enter":
                new_event["input"] = event.text_input

        self.events.append(new_event)


    def save_test(self):
        self.test["events"] = self.events
        self.document["test"] = self.test
        output = json.dumps(self.document, sort_keys=False, indent=4)
        filename = "generated_tests/{}/{}/android-to-ios/generated_test.json".format(self.app_name, self.test_name)
        print(output)
        if not os.path.exists(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        else:
            print("Removing Old Tests....")
            os.remove(filename)
        with open(filename, "w") as fw:
            fw.write(output)
            print("Writing to {}....".format(filename))



