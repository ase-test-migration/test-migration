import re
import dot_element_extract as dotElementExtractor

class Node:
    def __init__(self, id, attributes, interactable, interactions, num_of_children, tag, screenshot):
        self.id = id
        self.attributes = attributes
        self.interactable = interactable
        self.children = []
        self.parent = None
        self.interactions = interactions
        self.num_of_children = num_of_children
        self.tag = tag
        self.data = {}
        self.exec_identifier = {}
        self.sentence = []
        self.path_to_screenshot = screenshot

    def add_child(self, child_node):
        self.children.append(child_node)

    def add_data(self, key, value):
        self.data[key]=value

    def get_node_date(self):
        return self.data

    def get_attribute(self, key):
        return self.attributes[key]

    def add_exec_identifier(self, key, value):
        self.exec_identifier[key] = value

    def get_exec_identifiers(self):
        return self.exec_identifier

    def add_to_sentence(self, val):
        if "is not selected" in val:
            val = re.sub('is not selected$', '', val)
        if "is selected" in val:
            val = re.sub('is selected$', '', val)
        if re.match('^(?=.*(Tab [1-9] of [1-9],)).*$', val):
            val = re.sub('Tab [1-9] of [1-9], ', '', val)
        val="Click on "+val
        self.sentence.append(val)

    def get_sentence(self, turn):
        if turn>len(self.sentence):
            return ""
        else:
            return self.sentence[turn-1]

    def get_path_to_screenshot(self):
        return self.path_to_screenshot


    def get_exec_id_type(self):
        if len(list(self.exec_identifier.keys()))==0:
            return "xPath"
        else:
            return list(self.exec_identifier.keys())[0]

    def get_exec_id_val(self):
        if len(list(self.exec_identifier.keys())) == 0:
            #xpath, jsonlist = dotElementExtractor.findXPath(self.path_to_screenshot, self.get_path_to_dot())
            return None
        else:
            print("end of get_exec")
            return self.exec_identifier[list(self.exec_identifier.keys())[0]]

    def get_path_to_dot(self):
        print(self.path_to_screenshot)
        dot_path = self.path_to_screenshot.rsplit("/", 2)[0]
        dot_path += "/graph.dot"
        return dot_path