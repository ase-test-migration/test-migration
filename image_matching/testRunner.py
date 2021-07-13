import argparse
import os

import matplotlib as plt

import keypoint_comparator

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--android", required=True, help="Android test folder path")
ap.add_argument("-i", "--ios", required=True, help="iOS test folder path")
args = vars(ap.parse_args())

android_test_folder_path = args["android"]
ios_test_folder_path = args["ios"]

num_of_test_cases = len(os.listdir(android_test_folder_path))
print(num_of_test_cases)

if not os.path.isdir("outputs"):
    os.makedirs("outputs")

for subdir in os.listdir(android_test_folder_path):
    if subdir == ".DS_Store":
        continue

    if os.path.isdir(os.path.join("outputs", subdir)):
        continue
    os.makedirs(os.path.join("outputs", subdir))
    print("test name: "+subdir)
    num_of_events = len(os.listdir(os.path.join(android_test_folder_path, subdir)))
    num_of_successfully_transferred_events_android_to_ios = 0
    num_of_successfully_transferred_events_ios_to_android = 0

    for state in sorted(os.listdir(os.path.join(android_test_folder_path, subdir))):
        if not os.path.isdir(os.path.join("outputs", subdir, state)):
            os.makedirs(os.path.join("outputs", subdir, state))
        if state == ".DS_Store":
            continue
        print("state: "+state)
        with open(os.path.join(android_test_folder_path, subdir, state, "event_metadata.txt")) as metadata_file:
            metadata_file_content = metadata_file.readline()
            android_widget_image = ((metadata_file_content.split(": "))[1])[:-2]
            print("android_widget_image: "+android_widget_image)
        with open(os.path.join(ios_test_folder_path, subdir, state, "event_metadata.txt")) as metadata_file:
            metadata_file_content = metadata_file.readline()
            ios_widget_image = ((metadata_file_content.split(": "))[1])[:-2]
            print("ios_widget_image: "+ios_widget_image)
        ios_pngs_path = os.path.join(ios_test_folder_path, subdir, state, "pngs/")
        android_pngs_path = os.path.join(android_test_folder_path, subdir, state, "pngs/")

        android_widget_image_path = os.path.join(android_test_folder_path, android_widget_image)
        print("android_widget_image_path: "+android_widget_image_path)
        ios_widget_image_path = os.path.join(ios_test_folder_path, ios_widget_image)

        ios_matched_widget, ios_comparison_image = keypoint_comparator.find_matching_widget(android_widget_image_path, ios_pngs_path)
        android_matched_widget, android_comparison_image = keypoint_comparator.find_matching_widget(ios_widget_image_path, android_pngs_path)


        output_file = open(os.path.join("outputs", subdir, state, "transfer_results.txt"),"w")
        if ios_matched_widget and android_matched_widget:
          output_file.write("android widget image path: "+android_widget_image_path+ " - ios match widget path: "+ios_matched_widget+"\n"+"android match widget path "+ android_matched_widget + "ios widget image path: "+ ios_widget_image_path)
        output_file.close()

        if android_matched_widget:
            plt.image.imsave(os.path.join("outputs", subdir, state, "android_comparison.png"), android_comparison_image)
        if ios_matched_widget:
            plt.image.imsave(os.path.join("outputs", subdir, state, "ios_comparison.png"), ios_comparison_image)

        # android_comparison_file = open(os.path.join("outputs", subdir, state, "android_comparison.png"),"wb")
        # w = png.Writer(android_comparison_image.shape[0], android_comparison_image.shape[1], greyscale=True)
        # w.write(android_comparison_file, android_comparison_image)
        # android_comparison_file.close()
        #
        # ios_comparison_file = open(os.path.join("outputs", subdir, state, "ios_comparison.png"),"w")
        # ios_comparison_file.write(ios_comparison_image)
        # ios_comparison_file.close()





        # if ios_matched_widget == android_widget_image_path:
        #     num_of_successfully_transferred_events_android_to_ios = num_of_successfully_transferred_events_android_to_ios+1
        #     print("successful transfer from android to ios on state "+ state+ " for test "+ subdir)
        # else:
        #     plt.imshow(ios_comparison_image),plt.show()
        #
        # if android_matched_widget == ios_widget_image_path:
        #     num_of_successfully_transferred_events_ios_to_android = num_of_successfully_transferred_events_ios_to_android+1
        #     print("successful transfer from ios to android on state "+ state+ " for test "+ subdir)
        # else:
        #     plt.imshow(android_comparison_image),plt.show()











