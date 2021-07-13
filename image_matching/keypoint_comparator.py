import cv2
import matplotlib.pyplot as plt
import argparse
import glob
import pytesseract
import numpy as np
import imageio
from collections import Counter
import operator
import re


def dark_background(imagePath):
    image = imageio.imread(imagePath, as_gray=True)
    return np.mean(image) < 127


def OCR(self, h, w):
    image = cv2.imread(self)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imagem = imageio.imread(self, as_gray=True)
    #plt.imshow(imagem, 'gray'), plt.show()
    is_dark = np.mean(imagem) < 127
    if is_dark:
        print("black background")
        image = cv2.bitwise_not(image)
    #plt.imshow(image, 'gray'), plt.show()
    ocrResult=pytesseract.image_to_string(image)
    if not ocrResult:
        #print("[OCR] OCR cannot find any Text in this element.")
        return ocrResult
    proc_ocr_text=ocrResult.replace('\r', ' ').replace('\n', ' ').replace('\"', '\'').replace('<', '').replace('>','')
    if len(proc_ocr_text)>50:
        proc_ocr_text=proc_ocr_text[:50]+"..."
    #return proc_ocr_text, proc_ocr_text2
    return proc_ocr_text

def extract_position(image_path):
    name = image_path.split("/")
    image_name = name[-1]
    if image_name.endswith('.png'):
        image_name = image_name[:-4]
    #print(image_name)
    coordinates = image_name.split("_")
    coordinates = coordinates[0:4]
    return coordinates

def calc_image_size(image_path):
    coordinates = extract_position(image_path)
    top_left_x = float(coordinates[0])
    top_left_y = float(coordinates[1])
    bottom_right_x = float(coordinates[2])
    bottom_right_y = float(coordinates[3])
    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y
    return width * height

def find_distance_with_template(position, template_coordinates):
    #print(position)
    top_left_x = float(position[0])
    top_left_y = float(position[1])
    template_x = float(template_coordinates[0])
    template_y = float(template_coordinates[1])
    # template_x = float(args["x"])
    # template_y = float(args["y"])
    return ((template_x - top_left_x)**2) + ((template_y - top_left_y)**2)


def find_matching_widget(source_widget_path, destination_widget_directory):
    MIN_MATCH_COUNT = 10

    # sift = cv2.xfeatures2d.SIFT_create()
    # surf = cv2.xfeatures2d.SURF_create()


    print(source_widget_path)
    print(destination_widget_directory)
    orb = cv2.ORB_create()

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    scores = {}
    min_score = 100000



    template_path = source_widget_path
    template = cv2.imread(template_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    if dark_background(template_path):
        print("template is dark")
        template = cv2.bitwise_not(template)
    #template = cv2.Canny(template, 50, 200)
    template = cv2.GaussianBlur(template,(5,5),cv2.BORDER_DEFAULT)
    (tH, tW) = template.shape[:2]
    #plt.imshow(template, 'gray'), plt.show()
    template_text= OCR(template_path, tH, tW)
    template_text = re.sub(r"([0-9 :]+(\.[0-9 :]+)?)", r" \1 ", template_text).strip()

    if template_text:
        template_text = template_text.lower()


    template_coordinates = extract_position(template_path)
    template_size = calc_image_size(template_path)

    keypoints_1, descriptors_1 = orb.detectAndCompute(template, None)

    # keypoints_1, descriptors_1 = sift.detectAndCompute(template, None)

    exact_text_match_images = []
    good_matches = {}
    average_matches = {}
    good_text_matches = {}
    average_text_matches = {}
    match_found_in_text = False
    exact_text_match_found = False
    max_common = 0

    if template_text:
        print("template has text:"+ template_text)
        for imagePath in  glob.glob(destination_widget_directory + "/*.png"):
            image = cv2.imread(imagePath)
            image_text= OCR(imagePath, image.shape[0], image.shape[1])
            image_text = re.sub(r"([0-9 :]+(\.[0-9 :]+)?)",r" \1 ", image_text).strip()
            if image_text:
                image_text = image_text.lower()
                if image_text == template_text:
                    print("exact match: "+image_text)
                    exact_text_match_images.append(imagePath)
                else:
                    template_words = set(template_text.split())
                    image_words = set(image_text.split())
                    common = template_words & image_words
                    if len(common)>0:
                        print(len(common))
                        if float(len(common))/len(image_words)>max_common:
                            max_common = float(len(common))/len(image_words)
                        match_found_in_text = True
                        print("good text match: "+image_text)
                        good_text_matches[imagePath] = float(len(common))/len(image_words)
                    # else:
                    #     dict1 = Counter(image_text)
                    #     dict2 = Counter(template_text)
                    #     # take intersection of these dictionaries
                    #     common = dict1 & dict2
                    #     if len(common)>0:
                    #         match_found_in_text = True
                    #         average_text_matches[imagePath] = len(common)
                    #print("template text: " + template_text + "= image text: " + image_text + "- len common: "+ str(len(common)))

    if template_text:
        if len(exact_text_match_images)>0:
            print("We have an exact match")
            exact_text_match_found = True
        #print("We have exact an exact text match!")
            top_matches = exact_text_match_images
            match_found_in_text = True
        elif len(good_text_matches)>0:
            print(max_common)
            # top_matches = [image for image, common in good_text_matches.items() if common == max_common]
            print(good_text_matches)
            top_matches = sorted(good_text_matches, key=good_text_matches.get, reverse=True)
            print(top_matches)


    if not match_found_in_text:
        print("should use image matching")
        for imagePath in glob.glob(destination_widget_directory + "/*.png"):
            image = cv2.imread(imagePath)
            if dark_background(imagePath):
                image = cv2.bitwise_not(image)
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #image = cv2.Canny(image_gray, 50, 200)
            image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
            (iH, iW) = image.shape[:2]

            # keypoints_2, descriptors_2 = sift.detectAndCompute(image, None)
            keypoints_2, descriptors_2 = orb.detectAndCompute(image, None)

            if descriptors_2 is None:
                continue

            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
            search_params = dict(checks=50)

            # flann = cv2.FlannBasedMatcher(index_params, search_params)
            # if len(keypoints_1)<2 or len(keypoints_2)<2:
            #     continue
            # matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

            #print(matches)

            # bf matching
            # matches = sorted(matches, key = lambda x:x.distance)
            matches = bf.match(descriptors_1, descriptors_2)
            matches = sorted(matches, key = lambda x:x.distance)
            score = 0
            for match in matches[:5]:
                score = score + match.distance

            scores[imagePath] = score
            #========================
        #     good=[]
        #     for m, n in matches:
        #         if m.distance < 0.7 * n.distance:
        #             good.append(m)
        #
        #     draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
        #                        singlePointColor=None,
        #                        flags=2)
        #     img3 = cv2.drawMatches(template, keypoints_1, image, keypoints_2, good, None, **draw_params)
        #     plt.imshow(img3, 'gray'), plt.show()
        #
        #     if len(good) > MIN_MATCH_COUNT:
        #         good_matches[imagePath]=len(good)
        #
        #     if len(good) > 0:
        #         average_matches[imagePath]=len(good)
        #     else:
        #         matchesMask = None
        # top_matches = sorted(good_matches, key=good_matches.get)
            #===========================
            if score < min_score:
                min_score = score
                best_match = imagePath

    #print(scores)
        sorted_matched_widgets = sorted(scores, key=scores.get)
        #top k matches between extracted widgets from platdorm B based on keypoints similarity to template widget from platform A
        number_of_top_matches = 10

        top_matches = sorted_matched_widgets[:number_of_top_matches]
        top_matches = sorted_matched_widgets
    #print(top_matches)
    # print("---------------------")
    # print(top_matches)
    # print("---------------------")
    #print(top_matches)

    #sort the k top matches based on the physical place similarity to template widget on platform A
    physical_distance = {}
    size_differences = {}


    #print(top_matches)
    if len(top_matches)==0:
        top_matches = sorted(average_matches, key=average_matches.get)

    for tm in top_matches:
        #print(tm)
        position = extract_position(tm)
        size = calc_image_size(tm)
        #print(size)
        #change how distance being calculated
        distance = find_distance_with_template(position, template_coordinates)
        size_difference = abs(size - template_size)
        #print(tm+":"+str(distance)+ " -- " + str(size_difference))
        physical_distance[tm] = distance
        size_differences[tm] = size_difference


    sorted_matches_based_on_physical_distance = sorted(physical_distance, key=physical_distance.get)
    #print(sorted_matches_based_on_physical_distance)

    sorted_matches_based_on_size_difference = sorted(size_differences, key=size_differences.get)
    #print(sorted_matches_based_on_size_difference)

    average_rankings = {}
    if exact_text_match_found:
        for tm in top_matches:
            average_rankings[tm] = (sorted_matches_based_on_size_difference.index(tm)+sorted_matches_based_on_physical_distance.index(tm))/2
    else:
        for tm in top_matches:
            average_rankings[tm] = (2*sorted_matches_based_on_size_difference.index(tm)+2*sorted_matches_based_on_physical_distance.index(tm)+ top_matches.index(tm))/5
        #print(tm+":"+str(average_rankings[tm]))

    sorted_matches_based_on_size_and_position_average = sorted(average_rankings, key=average_rankings.get)
    #print(sorted_matches_based_on_size_and_position_average)



    #best_match = sorted_matched_widgets[0]
    #best_match = sorted_matches_based_on_physical_distance[0]
    if len(sorted_matches_based_on_size_and_position_average)==0:
        return None, None
    best_match = sorted_matches_based_on_size_and_position_average[0]
    # print(best_match)
    img2 = cv2.imread(best_match)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    if dark_background(best_match):
        img2 = cv2.bitwise_not(img2)
    #img2 = cv2.Canny(img2, 50, 200)
    img2 = cv2.GaussianBlur(img2,(5,5),cv2.BORDER_DEFAULT)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
    matches = bf.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)

    img3 = cv2.drawMatches(template, keypoints_1, img2, keypoints_2, matches[:10], img2, flags=2)
    # print(type(img3))
    # plt.imshow(img3),plt.show()
    # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
    #                    singlePointColor=None,
    #                    flags=2)
    # img3 = cv2.drawMatches(template, keypoints_1, img2, keypoints_2, good, None, **draw_params)
    #plt.imshow(img3, 'gray'), plt.show()


    return best_match, img3











