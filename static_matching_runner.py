import argparse
import os
from image_matching import similarity_calculator
import matplotlib as plt
import png
import glob
from sys import argv
import json
from text_matching import text_similarity_calculator
import time
from text_matching import text_utils
from shutil import copyfile

text_sim_calc = text_similarity_calculator.SimilarityCalculator()
def get_element_max_similarity(element_text_dict, event_text_dict):
    max_score = 0
    for key1, event_text in event_text_dict.items():
        for key2, element_text in element_text_dict.items():
            score = text_sim_calc.calc_similarity(event_text, element_text)
            if score > max_score:
                max_score = score
    return max_score

def find_matching(android_state_num, ios_state_num, test_name):
    output_file_name = "android_S"+str(android_state_num)+"_ios_S"+str(ios_state_num)
    os.makedirs(os.path.join("staticout", test_name, output_file_name))

    with open(os.path.join(android_test_folder_path, "S"+str(android_state_num), "event_metadata.txt")) as android_metadata_file:
        metadata_file_content = android_metadata_file.readline()
        print(metadata_file_content)
        android_widget_image = ((metadata_file_content.split(": "))[1])[:-2]
        metadata_file_coordinates = android_metadata_file.readline()
        android_metadata_file_text_identifier = android_metadata_file.readline()
        android_metadata_file_event = android_metadata_file.readline()
        android_metadata_file_event = ((android_metadata_file_event.split(": "))[1])[:-2]
        if android_metadata_file_event == "send_keys":
            android_text_input = android_metadata_file.readline()
            android_text_input = ((android_text_input.split(": "))[1])[:-2]
        if android_metadata_file_event == "back":
            android_widget_image = "pathToElementImageCrop: resources/0_2000_1_2001.png"
            android_metadata_file_text_identifier = 'text_identifier: { "name" : "back" }; '

        android_widget_image = android_widget_image.split("/", 1)[1]
        print("android widget image:")
        print(android_widget_image)

        android_widget_text_ids = (android_metadata_file_text_identifier.partition(":")[2])[:-2]
        android_text_ids_dict = json.loads(android_widget_text_ids)
        android_text_ids_dict = text_utils.preprocess_info_dict(android_text_ids_dict)
        print(android_text_ids_dict)

    ios_to_android_texts_dict = {}
    with open(os.path.join(android_test_folder_path, "S" + str(android_state_num),
                           "texts.txt")) as android_texts_file:
        lines = [line.rstrip('\n') for line in android_texts_file]
        for line in lines:
            print(line)
            line_dict = json.loads(line)
            text_dict = {}
            for key,value in line_dict.items():
                if key!="screenshotPath":
                    text_dict[key]=value
            ios_to_android_texts_dict[line_dict["screenshotPath"]] = text_dict

    print(ios_to_android_texts_dict)


    with open(os.path.join(ios_test_folder_path, "S"+str(ios_state_num), "event_metadata.txt")) as ios_metadata_file:
        metadata_file_content = ios_metadata_file.readline()
        ios_widget_image = ((metadata_file_content.split(": "))[1])[:-2]
        ios_widget_image = ios_widget_image.split("/", 1)[1]
        print("ios_widget_image:")
        print(ios_widget_image)
        ios_metadata_file_coordinates = ios_metadata_file.readline()
        ios_metadata_file_text_identifier = ios_metadata_file.readline()
        ios_metadata_file_event = ios_metadata_file.readline()
        ios_metadata_file_event = ((ios_metadata_file_event.split(": "))[1])[:-2]
        print("text_identifieer")
        print(ios_metadata_file_text_identifier)
        if ios_metadata_file_event == "send_keys":
            ios_text_input = ios_metadata_file.readline()
            ios_text_input = ((ios_text_input.split(": "))[1])[:-2]
        ios_widget_text_ids = (ios_metadata_file_text_identifier.partition(":")[2])[:-2]
        print(ios_widget_text_ids)
        ios_text_ids_dict = json.loads(ios_widget_text_ids)
        print(ios_text_ids_dict)
        ios_text_ids_dict = text_utils.preprocess_info_dict(ios_text_ids_dict)
        print(ios_text_ids_dict)
        # print("widget_text_id: " + widget_text_id)

    android_to_ios_texts_dict = {}
    with open(os.path.join(ios_test_folder_path, "S" + str(ios_state_num),
                           "texts.txt")) as ios_texts_file:
        lines = [line.rstrip('\n') for line in ios_texts_file]
        for line in lines:
            print(line)
            line_dict = json.loads(line)
            text_dict = {}
            for key, value in line_dict.items():
                if key != "screenshotPath":
                    text_dict[key] = value
            android_to_ios_texts_dict[line_dict["screenshotPath"]] = text_dict

    print(android_to_ios_texts_dict)

    ios_pngs_path = os.path.join(ios_test_folder_path, "S"+str(ios_state_num), "pngs/")
    android_pngs_path = os.path.join(android_test_folder_path, "S"+str(android_state_num), "pngs/")

    if android_metadata_file_event == "back":
        android_widget_image_path = os.path.join(android_test_folder_path, "../resources", android_widget_image)
    else:
        android_widget_image_path = os.path.join(android_test_folder_path, android_widget_image)
    ios_widget_image_path = os.path.join(ios_test_folder_path, ios_widget_image)

    print("android widget image path: ")
    print(android_widget_image_path)
    print("ios widget image path: ")
    print(ios_widget_image_path)

    android_to_ios_max_score_img = None
    android_to_ios_max_visual_similarity_score = 0
    android_to_ios_visual_element_score = {}
    android_to_ios_textual_element_score = {}
    android_to_ios_only_visual_element_score = {}
    for ios_image_path in glob.glob(ios_pngs_path + "/*.png"):
        print(ios_image_path)
        exact_text_match, common_words, proximity_score, size_similarity_score, image_similarity_score, edit_distance, ocr_output, source_ocr, img3 = similarity_calculator.calc_score(android_widget_image_path, ios_image_path, 1)
        if source_ocr != "":
            android_text_ids_dict["ocr"] = source_ocr
        if ocr_output != "":
            if ios_image_path.split("/", 1)[1] in android_to_ios_texts_dict.keys():
                elem_text_dict = android_to_ios_texts_dict[ios_image_path.split("/", 1)[1]]
            else:
                elem_text_dict = {}
            elem_text_dict["ocr"] = ocr_output
            print("##")
            print(elem_text_dict)
            android_to_ios_texts_dict[ios_image_path.split("/", 1)[1]]=elem_text_dict
        visual_similarity_score = (5 * image_similarity_score + 3 * proximity_score + 2 * size_similarity_score) / 8
        for_only_visual_score =  (5 * image_similarity_score + 3 * proximity_score + 2 * size_similarity_score + 3*edit_distance) / 11
        if visual_similarity_score > android_to_ios_max_visual_similarity_score:
            android_to_ios_max_visual_similarity_score = visual_similarity_score
            android_to_ios_max_score_img = img3
        android_to_ios_visual_element_score[ios_image_path] = visual_similarity_score
        android_to_ios_only_visual_element_score[ios_image_path] = for_only_visual_score
        if ios_image_path.split("/", 1)[1] in android_to_ios_texts_dict.keys():
            print("##")
            print(android_to_ios_texts_dict[ios_image_path.split("/", 1)[1]])
            textual_similarity = get_element_max_similarity(android_to_ios_texts_dict[ios_image_path.split("/", 1)[1]], android_text_ids_dict)
        else:
            textual_similarity = 0
        android_to_ios_textual_element_score[ios_image_path] = textual_similarity


    android_to_ios_visually_sort_by_scores = sorted(android_to_ios_visual_element_score, key=android_to_ios_visual_element_score.get)
    android_to_ios_textually_sort_by_scores = sorted(android_to_ios_textual_element_score, key=android_to_ios_textual_element_score.get)
    android_to_ios_only_visually_sort_by_scores = sorted(android_to_ios_only_visual_element_score, key=android_to_ios_only_visual_element_score.get)
    print(android_to_ios_texts_dict)
    print("------------------ visually ranked -----------------")
    for ranked in android_to_ios_visually_sort_by_scores:
        print(ranked)
    print("------------------ textually ranked -----------------")
    for ranked in android_to_ios_textually_sort_by_scores:
        print(ranked)
    ios_to_android_max_score_img = None
    ios_to_android_max_visual_similarity_score = 0
    ios_to_android_visual_element_score = {}
    ios_to_android_textual_element_score = {}
    ios_to_android_only_visual_element_score = {}
    source_ocr=""
    for android_image_path in glob.glob(android_pngs_path + "/*.png"):
        exact_text_match, common_words, proximity_score, size_similarity_score, image_similarity_score, edit_distance, ocr_output, source_ocr, android_img = similarity_calculator.calc_score(ios_widget_image_path, android_image_path, 2)
        if source_ocr != "":
            ios_text_ids_dict["ocr"] = source_ocr
        if ocr_output != "":
            if android_image_path.split("/", 1)[1] in ios_to_android_texts_dict.keys():
                elem_text_dict = ios_to_android_texts_dict[android_image_path.split("/", 1)[1]]
            else:
                elem_text_dict = {}
            elem_text_dict["ocr"] = ocr_output
            ios_to_android_texts_dict[android_image_path.split("/", 1)[1]]=elem_text_dict
        visual_similarity_score = (5 * image_similarity_score + 3 * proximity_score + 2 * size_similarity_score) / 8
        for_only_visual_score =  (5 * image_similarity_score + 3 * proximity_score + 2 * size_similarity_score + 3*edit_distance) / 11
        print("proximity_score:")
        print(proximity_score)
        print("size_similarity_score:")
        print(size_similarity_score)
        print("vis_sim_score:")
        print(visual_similarity_score)
        ios_to_android_visual_element_score[android_image_path] = visual_similarity_score
        ios_to_android_only_visual_element_score[android_image_path] = for_only_visual_score
        if visual_similarity_score > ios_to_android_max_visual_similarity_score:
            ios_to_android_max_visual_similarity_score = visual_similarity_score
            ios_to_android_max_score_img = android_img

        if android_image_path.split("/", 1)[1] in ios_to_android_texts_dict.keys():
            textual_similarity = get_element_max_similarity(ios_to_android_texts_dict[android_image_path.split("/", 1)[1]],
                                                        ios_text_ids_dict)
        else:
            textual_similarity = 0
        ios_to_android_textual_element_score[android_image_path] = textual_similarity


    ios_to_android_visually_sort_by_scores = sorted(ios_to_android_visual_element_score, key=ios_to_android_visual_element_score.get)
    ios_to_android_textually_sort_by_scores = sorted(ios_to_android_textual_element_score, key=ios_to_android_textual_element_score.get)
    ios_to_android_only_visually_sort_by_scores = sorted(ios_to_android_only_visual_element_score, key=ios_to_android_only_visual_element_score.get)
    print(ios_to_android_texts_dict)
    print("------------------ visually ranked -----------------")
    for ranked in ios_to_android_visually_sort_by_scores:
        print(ranked)
    print("------------------ textually ranked -----------------")
    for ranked in ios_to_android_textually_sort_by_scores:
        print(ranked)
    #android to ios result
    android_to_ios_best_only_text = android_to_ios_textually_sort_by_scores[-1]
    android_to_ios_best_only_vision = android_to_ios_visually_sort_by_scores[-1]
    android_to_ios_best_only_vision_ocr = android_to_ios_only_visually_sort_by_scores[-1]
    if android_to_ios_visually_sort_by_scores[-1] == android_to_ios_textually_sort_by_scores[-1]:
        android_to_ios_next_event_widget = android_to_ios_textually_sort_by_scores[-1]
    else:
        if android_to_ios_textual_element_score[android_to_ios_textually_sort_by_scores[-1]] >= 0.5:
            good_ios_text_matches = []
            for ios_element in android_to_ios_textually_sort_by_scores:
                if(android_to_ios_textual_element_score[android_to_ios_textually_sort_by_scores[-1]]-android_to_ios_textual_element_score[ios_element])<0.1:
                    good_ios_text_matches.append(ios_element)

            highest_vis_score = 0
            for good_ios_text_match in good_ios_text_matches:
                if android_to_ios_visual_element_score[good_ios_text_match] > highest_vis_score:
                    highest_vis_score = android_to_ios_visual_element_score[good_ios_text_match]
                    android_to_ios_next_event_widget = good_ios_text_match

            # if (android_to_ios_textual_element_score[android_to_ios_textually_sort_by_scores[-1]] - android_to_ios_textual_element_score[android_to_ios_textually_sort_by_scores[-2]])<0.1:
            #     if android_to_ios_visual_element_score[android_to_ios_textually_sort_by_scores[-1]]>android_to_ios_visual_element_score[android_to_ios_textually_sort_by_scores[-2]]:
            #         android_to_ios_next_event_widget = android_to_ios_textually_sort_by_scores[-1]
            #     else:
            #         android_to_ios_next_event_widget = android_to_ios_textually_sort_by_scores[-2]
            # else:
            #     android_to_ios_next_event_widget = android_to_ios_textually_sort_by_scores[-1]
        else:
            android_to_ios_next_event_widget = android_to_ios_visually_sort_by_scores[-1]

    #ios to android result
    ios_to_android_best_only_text = ios_to_android_textually_sort_by_scores[-1]
    ios_to_android_best_only_vision = ios_to_android_visually_sort_by_scores[-1]
    ios_to_android_best_only_vision_ocr = ios_to_android_only_visually_sort_by_scores[-1]
    if ios_to_android_visually_sort_by_scores[-1] == ios_to_android_textually_sort_by_scores[-1]:
        ios_to_android_next_event_widget = ios_to_android_textually_sort_by_scores[-1]
    else:
        good_android_text_matches = []
        if ios_to_android_textual_element_score[ios_to_android_textually_sort_by_scores[-1]] >= 0.5:
            for android_element in ios_to_android_textually_sort_by_scores:
                if(ios_to_android_textual_element_score[ios_to_android_textually_sort_by_scores[-1]]-ios_to_android_textual_element_score[android_element])<0.1:
                    good_android_text_matches.append(android_element)

            highest_vis_score = 0
            for good_android_text_match in good_android_text_matches:
                if ios_to_android_visual_element_score[good_android_text_match]>highest_vis_score:
                    highest_vis_score = ios_to_android_visual_element_score[good_android_text_match]
                    ios_to_android_next_event_widget = good_android_text_match
            # if (ios_to_android_textual_element_score[ios_to_android_textually_sort_by_scores[-1]]-ios_to_android_textual_element_score[ios_to_android_textually_sort_by_scores[-2]])<0.1:
            #     if ios_to_android_visual_element_score[ios_to_android_textually_sort_by_scores[-1]]>ios_to_android_visual_element_score[ios_to_android_textually_sort_by_scores[-2]]:
            #         ios_to_android_next_event_widget = ios_to_android_textually_sort_by_scores[-1]
            #     else:
            #         ios_to_android_next_event_widget = ios_to_android_textually_sort_by_scores[-2]
            # else:
            #     ios_to_android_next_event_widget = ios_to_android_textually_sort_by_scores[-1]
        else:
            ios_to_android_next_event_widget = ios_to_android_visually_sort_by_scores[-1]

    out_path = "staticout/"+test_name+"/android_S"+str(android_state_num)+"_ios_S"+str(ios_state_num)
    print("out path:")
    print(out_path)
    print(ios_to_android_next_event_widget)
    print(android_to_ios_next_event_widget)

    copyfile(android_widget_image_path, out_path + "/android.png")
    copyfile(ios_to_android_next_event_widget, out_path+"/ios_to_android.png")
    copyfile(ios_to_android_best_only_text, out_path + "/ios_to_android_best_only_text.png")
    copyfile(ios_to_android_best_only_vision, out_path + "/ios_to_android_best_only_vision.png")
    copyfile(ios_to_android_best_only_vision_ocr, out_path + "/ios_to_android_best_only_vision_ocr.png")
    copyfile(ios_widget_image_path, out_path + "/ios.png")
    copyfile(android_to_ios_next_event_widget, out_path+"/android_to_ios.png")
    copyfile(android_to_ios_best_only_text, out_path+"/android_to_ios_best_only_text.png")
    copyfile(android_to_ios_best_only_vision, out_path+"/android_to_ios_best_only_vision.png")
    copyfile(android_to_ios_best_only_vision_ocr, out_path+"/android_to_ios_best_only_vision_ocr.png")
    # if ios_to_android_max_score_img is not None:
    #     plt.image.imsave(out_path+"/ios_to_android_comparison", ios_to_android_max_score_img)
    # if android_to_ios_max_score_img is not None:
    #     plt.image.imsave(out_path+"/android_to_ios_comparison", android_to_ios_max_score_img)

    # print("result:")
    # print(android_to_ios_visually_sort_by_scores[-1])
    # if android_to_ios_max_score_img is not None:
    #     plt.image.imsave(os.path.join("staticout", test_name, output_file_name, "android_to_ios.png"), android_to_ios_max_score_img)
    # if ios_to_android_max_score_img is not None:
    #     plt.image.imsave(os.path.join("staticout", test_name, output_file_name, "ios_to_android.png"), ios_to_android_max_score_img)


if __name__ == "__main__":
    android_test_folder_path = argv[1]
    ios_test_folder_path = argv[2]
    test_name = argv[3]
    print(android_test_folder_path)
    print(ios_test_folder_path)
    states = [3]
    failed_states={}
    for state in states:
    #     try:
        find_matching(state, state, test_name)
    #     except json.decoder.JSONDecodeError as e:
    #         print("ERROR: STATE {} Failed. Failed to parse json".format(state))
    #         failed_states[state]=e
    #         continue
    #     except IndexError as e:
    #         print("ERROR: STATE {} Failed. METADATA FILE MAY CONTAIN NEWLINE. ".format(state))
    #         failed_states[state]=e
    #         continue
    #     except FileNotFoundError:
    #         print("Total: {} Attempts, {} States Migrated.".format(state, state-len(failed_states)))
    #         print("Removing Blank Folder...")
    #         os.removedirs(os.path.join("staticout", test_name, "android_S"+str(state)+"_ios_S"+str(state)))
    #         break
    # print("Failed States:")
    # for key, value in failed_states.items():
    #     print("STATE {}: {}".format(key,value))

