from sys import argv
import os
import re
import explorer
from image_matching import similarity_calculator
from text_matching import text_similarity_calculator
import time
from text_matching import text_utils
import json
import selenium
import test_generator
from selenium.webdriver.common.keys import Keys
import os.path
from os import path


def generate_output_folder():
    if not os.path.isdir("outputs"):
        os.makedirs("outputs")


class TestCase:
    def __init__(self, test_folder_path):
        self.test_folder_path = test_folder_path
        self.events = []

    def add_event(self, action, state, image_path, text, text_input):
        event = Event(action, state, image_path, text, text_input)
        self.events.append(event)

    def print_test_case(self):
        for event in self.events:
            print("--------------------")
            print("state: " + event.state)
            print("action: " + event.action)
            print("image_path: " + event.image_path)
            print(event.text)


class Event:
    def __init__(self, action, state, image_path, text, text_input):
        self.action = action
        self.state = state
        self.image_path = image_path
        self.text = text
        self.text_input = text_input


class DestEvent:
    def __init__(self, action, exec_id_type, exec_id_val, text_input):
        self.action = action
        self.exec_id_type = exec_id_type
        self.exec_id_val = exec_id_val
        self.text_input = text_input

    def print_event(self):
        print("---- printing dest event ----")
        print("action:")
        print(self.action)
        print("exec_id_type")
        print(self.exec_id_type)
        print("exec_id_val")
        print(self.exec_id_val)
        print("text_input")
        print(self.text_input)


class Migrator:
    def __init__(self, source_test_folder_path):
        self.source_test_folder_path = source_test_folder_path
        generate_output_folder()
        self.source_test = self.make_source_sequence()
        self.source_test.print_test_case()
        self.text_sim_calc = text_similarity_calculator.SimilarityCalculator()
        self.test_generator = test_generator.TestGenerator(source_test_folder_path,
                                                           self.source_test_folder_path.split("/")[-1], )
        self.mappable_attributes = {"resource-id", "text", "enabled", "content-descriptor", "visible", "selected",
                                    "checked"}
        self.mapped_negative_oracles = []

    def assert_equal_attribute_mapper(self, source_attribute):
        if source_attribute not in self.mappable_attributes:
            dest_attribute = "not_mappable"
        else:
            if source_attribute == "resource-id":
                dest_attribute = "name"
            elif source_attribute == "text":
                dest_attribute = "label"
            elif source_attribute == "enabled":
                dest_attribute = "enabled"
            elif source_attribute == "content-descriptor":
                dest_attribute = "accessibility-id"
            elif source_attribute == "visible":
                dest_attribute = "displayed"
            elif source_attribute == "selected":
                dest_attribute = "value"
            elif source_attribute == "checkable":
                dest_attribute = "value"
        return dest_attribute

    def make_source_sequence(self):
        test_case = TestCase(self.source_test_folder_path)
        test_name = self.source_test_folder_path.split("/")[-1]
        self.test_name = test_name
        # os.makedirs(os.path.join("outputs/android-to-ios", test_name))
        print("test name: " + test_name)
        for state in sorted(os.listdir(self.source_test_folder_path)):
            text_input = ""
            if not os.path.isdir(os.path.join("outputs/android-to-ios", test_name, state)):
                os.makedirs(os.path.join("outputs/android-to-ios", test_name, state))
            if state == ".DS_Store":
                continue
            # print("state: " + state)
            with open(os.path.join(self.source_test_folder_path, state,
                                   "event_metadata.txt")) as metadata_file:
                metadata_file_image_path = metadata_file.readline()
                metadata_file_coordinates = metadata_file.readline()
                metadata_file_text_identifier = metadata_file.readline()
                print("ovo je test: " + metadata_file_text_identifier)
                metadata_file_event = metadata_file.readline()
                # TODO: Fail when metadata event json contain newline
                metadata_file_event = ((metadata_file_event.split(": "))[1])[:-2]

                if metadata_file_event == "oracle":
                    oracle_type = metadata_file.readline()
                    oracle_type = (oracle_type.split(": ")[1])[:-2]
                    if oracle_type == "text_exists":
                        oracle_text = metadata_file.readline()
                        oracle_text = (oracle_text.split(": ")[1])[:-2]
                        test_case.add_event("oracle-text_exists", state, "", {}, oracle_text)
                    if oracle_type == "widget_exists":
                        widget_image_path = ((metadata_file_image_path.split(": "))[1])[:-2]
                        widget_text_ids = (metadata_file_text_identifier.partition(":")[2])[:-2]
                        text_ids_dict = json.loads(widget_text_ids)
                        text_ids_dict = text_utils.preprocess_info_dict(text_ids_dict)
                        test_case.add_event("oracle-widget_exists", state, widget_image_path, text_ids_dict, text_input)
                    if oracle_type == "element_invisible":
                        widget_image_path = ((metadata_file_image_path.split(": "))[1])[:-2]
                        widget_text_ids = (metadata_file_text_identifier.partition(":")[2])[:-2]
                        text_ids_dict = json.loads(widget_text_ids)
                        text_ids_dict = text_utils.preprocess_info_dict(text_ids_dict)
                        test_case.add_event("oracle-element_invisible", state, widget_image_path, text_ids_dict,
                                            text_input)
                    if oracle_type == "assert_equal":
                        widget_image_path = ((metadata_file_image_path.split(": "))[1])[:-2]
                        widget_text_ids = (metadata_file_text_identifier.partition(":")[2])[:-2]
                        text_ids_dict = json.loads(widget_text_ids)
                        text_ids_dict = text_utils.preprocess_info_dict(text_ids_dict)
                        assert_attribute = metadata_file.readline()
                        assert_attribute = (assert_attribute.split(": ")[1])[:-2]
                        assert_value = metadata_file.readline()
                        assert_value = (assert_value.split(": ")[1])[:-2]
                        text_input = assert_attribute + " : " + assert_value
                        test_case.add_event("oracle-assert_equal", state, widget_image_path, text_ids_dict, text_input)
                    if oracle_type == "text_invisible":
                        oracle_text = metadata_file.readline()
                        oracle_text = (oracle_text.split(": ")[1])[:-2]
                        test_case.add_event("oracle-text_invisible", state, "", {}, oracle_text)
                else:
                    if metadata_file_event == "back":
                        metadata_file_image_path = "pathToElementImageCrop: resources/0_2000_1_2001.png; "
                        metadata_file_text_identifier = 'text_identifier: { "name" : "back" }; '
                        metadata_file_event = "click"

                    widget_image_path = ((metadata_file_image_path.split(": "))[1])[:-2]
                    print("text_identifieer")
                    print(metadata_file_text_identifier)
                    if metadata_file_event == "send_keys" or metadata_file_event == "send_keys_enter":
                        text_input = metadata_file.readline()
                        text_input = ((text_input.split(": "))[1])[:-2]
                    widget_text_ids = (metadata_file_text_identifier.partition(":")[2])[:-2]
                    print(widget_text_ids)
                    try:
                        text_ids_dict = json.loads(widget_text_ids)
                        print(text_ids_dict)
                        text_ids_dict = text_utils.preprocess_info_dict(text_ids_dict)
                        print(text_ids_dict)
                        test_case.add_event(metadata_file_event, state, widget_image_path, text_ids_dict, text_input)
                    except ValueError:
                        print("There is no json value in text_ids_dict, probably this action is click by coordinate.")
                        text_ids_dict = {}
                        print(text_ids_dict)
                        # print("widget_text_id: " + widget_text_id)
                        test_case.add_event(metadata_file_event, state, widget_image_path, text_ids_dict, text_input)
        return test_case

    def start_dest_explorer(self):
        self.explorer = explorer.Explorer()

    def find_mapping_widgets_for_negative_oracles(self, negative_oracles, current_state):
        print("in find mapping")
        print(negative_oracles)
        for negative_oracle in negative_oracles:
            print(negative_oracle)
            event = self.source_test.events[negative_oracle]
            print(event.state)
            state_name_path = "outputs/ios-to-android/{}/{}".format(self.test_name, event.state)
            print("in mapping:")
            print(state_name_path)
            next_event = self.find_best_action(current_state, event, state_name_path, 1)
            mapped_oracle = {
                "id": event.state,
                "event": next_event
            }
            self.mapped_negative_oracles.append(mapped_oracle)

    def migrate(self, ):
        try:
            for index, event in enumerate(self.source_test.events):
                negative_oracles = []
                state_name_path = "outputs/android-to-ios/{}/{}".format(self.test_name, event.state)
                source_state_path = "{}/{}".format(self.source_test_folder_path, event.state)
                negative_oracle_file_path = source_state_path + "/negative_oracle_state_ids.txt"
                print("state name path : ***********")
                print(state_name_path)
                if path.exists(negative_oracle_file_path):
                    negative_oracle_file = open(negative_oracle_file_path, 'r')
                    lines = negative_oracle_file.readlines()
                    for line in lines:
                        negative_oracles.append(int(line))
                    print(negative_oracles)
                if event.action == "oracle-text_exists":
                    self.explorer.check_text_exist_assertion(event.text_input, state_name_path)
                    next_event = DestEvent("oracle-text_exists", "", "", event.text_input)
                    self.test_generator.add_step(next_event)
                elif event.action == "oracle-text_invisible":
                    self.explorer.check_text_invisible_assertion(event.text_input, state_name_path)
                    next_event = DestEvent("oracle-text_invisible", "", "", event.text_input)
                    self.test_generator.add_step(next_event)
                elif event.action == "oracle-element_invisible":
                    for negative_oracle in self.mapped_negative_oracles:
                        if negative_oracle["id"] == 'S' + str(index):
                            event = negative_oracle["event"]
                    self.explorer.check_element_invisible_assertion(event)
                    next_event = DestEvent("oracle-element_invisible", event.exec_id_type, event.exec_id_val, "")
                    self.test_generator.add_step(next_event)
                elif event.action == "back":
                    next_event = DestEvent("back", "", "", "")
                    self.explorer.execute_event(next_event)
                    self.test_generator.add_step(next_event)
                else:
                    time.sleep(15)
                    curr_state = self.explorer.extract_state(state_name_path)
                    curr_state.print_state()
                    i = 1
                    while True:
                        try:
                            next_event = self.find_best_action(curr_state, event, state_name_path, i)
                            if len(negative_oracles) > 0:
                                self.find_mapping_widgets_for_negative_oracles(negative_oracles, curr_state)
                            self.explorer.execute_event(next_event)
                            print("after execute")
                            break

                        except selenium.common.exceptions.InvalidElementStateException:
                            print("got the error")
                            i += 1
                            pass
                    self.test_generator.add_step(next_event)
        except Exception as e:
            print(e)
        finally:
            self.test_generator.save_test()

    def find_best_action(self, current_state, event, state_name_path, i):
        print("starting find beest")
        source_widget_path = "python-android/" + event.image_path
        destination_widgets_path = state_name_path + "/pngs"
        image_based_ranking, visual_scores, source_ocr = self.get_actions_visual_similarity_ranking(source_widget_path,
                                                                                                    current_state)
        if source_ocr != "":
            event.text["ocr"] = source_ocr
        text_based_ranking, textual_scores = self.get_actions_textual_similarity_ranking(event.text, current_state)
        while True:
            if i == 1:
                if text_based_ranking[-i] == image_based_ranking[-i]:
                    next_event_widget = text_based_ranking[-i]
                    print("same top rank")
                else:
                    if textual_scores[text_based_ranking[-i]] >= 0.5:
                        print("text based")
                        good_text_matches = []
                        for element in text_based_ranking:
                            if (textual_scores[text_based_ranking[-i]] - textual_scores[element]) < 0.1:
                                good_text_matches.append(element)
                        highest_vis_sim = 0
                        for good_match in good_text_matches:
                            if visual_scores[good_match] > highest_vis_sim:
                                highest_vis_sim = visual_scores[good_match]
                                next_event_widget = good_match
                    else:
                        next_event_widget = image_based_ranking[-i]
                        print("image based")
                    # elif visual_scores[image_based_ranking[-i]] >= 0.5:
                    #     next_event_widget = image_based_ranking[-i]
                    # else:
                    #     return None
            else:
                if textual_scores[text_based_ranking[-i]] >= 0.5:
                    next_event_widget = text_based_ranking[-i]
                else:
                    next_event_widget = image_based_ranking[-i]
                # elif visual_scores[image_based_ranking[-i]] >= 0.5:
                #     next_event_widget = image_based_ranking[-i]
                # print()
            if next_event_widget.get_exec_id_type() != "xPath":
                break
            print("not broken")
            i += 1
        if event.action == "oracle-assert_equal":
            attribute = event.text_input.split(" : ")[0]
            value = event.text_input.split(" : ")[1]
            dest_attribute = self.assert_equal_attribute_mapper(attribute)
            if dest_attribute == "name" or dest_attribute == "label":
                value = next_event_widget.get_attribute(dest_attribute)
            if dest_attribute == "not_mappable":
                new_text_input = dest_attribute
            else:
                new_text_input = dest_attribute + " : " + value
            next_event = DestEvent(event.action, next_event_widget.get_exec_id_type(),
                                   next_event_widget.get_exec_id_val(), new_text_input)
        else:
            next_event = DestEvent(event.action, next_event_widget.get_exec_id_type(),
                                   next_event_widget.get_exec_id_val(), event.text_input)
        return next_event

    def get_element_max_similarity(self, element_text_dict, event_text_dict):
        max_score = 0
        for key1, event_text in event_text_dict.items():
            for key2, element_text in element_text_dict.items():
                score = self.text_sim_calc.calc_similarity(event_text, element_text)
                if score > max_score:
                    max_score = score
        return max_score

    def get_actions_textual_similarity_ranking(self, event_text, destination_state):
        element_score = {}
        for element in destination_state.nodes:
            element_max_similarity = self.get_element_max_similarity(element.data, event_text)
            print("element_score:")
            print(element_max_similarity)
            element_score[element] = element_max_similarity

        sort_by_scores = sorted(element_score, key=element_score.get)
        print("------------------ textually ranked -----------------")
        for ranked in sort_by_scores:
            print(ranked.exec_identifier)
        print(sort_by_scores)
        return sort_by_scores, element_score

    def get_actions_visual_similarity_ranking(self, source_widget_path, destination_state):
        element_score = {}
        for element in destination_state.nodes:
            dest_widget_path = element.path_to_screenshot
            print(dest_widget_path)
            exact_text_match, common_words, proximity_score, size_similarity_score, image_similarity_score, edit_distance, ocr_output, source_output, img = similarity_calculator.calc_score(
                source_widget_path, dest_widget_path, 1)
            visual_similarity_score = (5 * image_similarity_score + 3 * proximity_score + 2 * size_similarity_score) / 8
            if ocr_output != "":
                element.add_data("ocr", ocr_output)
            print("visual_similarity_score:")
            print(visual_similarity_score)
            element_score[element] = visual_similarity_score

        sort_by_scores = sorted(element_score, key=element_score.get)
        print("------------------ visually ranked -----------------")
        for ranked in sort_by_scores:
            print(ranked.exec_identifier)
        print(sort_by_scores)
        return sort_by_scores, element_score, source_output


if __name__ == "__main__":
    start = time.time()
    migrator = Migrator(argv[1])
    migrator.start_dest_explorer()
    migrator.migrate()
    end = time.time()
    print("iOS migration running time " + str(end - start) + " seconds")
