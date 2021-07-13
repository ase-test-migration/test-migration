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
import editdistance
import time
import math


#set the screen size here for screen sizes below once and for all.
p_android_screen_x=1080
p_android_screen_y=1776
p_ios_screen_x=1242
p_ios_screen_y=2688

# p_android_screen_x=1080
# p_android_screen_y=2028
# p_ios_screen_x=750
# p_ios_screen_y=1334
#
# p_android_screen_x=1080
# p_android_screen_y=2400
# p_ios_screen_x=750
# p_ios_screen_y=1334

# p_android_screen_x=1080
# p_android_screen_y=2220
# p_ios_screen_x=750
# p_ios_screen_y=1334

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

def OCR(image_path, h, w):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imagem = imageio.imread(image_path, as_gray=True)
    #plt.imshow(imagem, 'gray'), plt.show()
    is_dark = np.mean(imagem) < 127
    if is_dark:
        image = cv2.bitwise_not(image)
    #plt.imshow(image, 'gray'), plt.show()
    ocrResult=pytesseract.image_to_string(image)
    if not ocrResult:
        #print("[OCR] OCR cannot find any Text in this element.")
        return ocrResult
    proc_ocr_text=ocrResult.replace('\r', ' ').replace('\n', ' ').replace('\"', '\'').replace('<', '').replace('>','')
    if len(proc_ocr_text)>50:
        proc_ocr_text=proc_ocr_text[:50]+"..."
    return proc_ocr_text

def dark_background(image_path):
    image = imageio.imread(image_path, as_gray=True)
    print(np.mean(image) < 127)
    return np.mean(image) < 127


def find_distance_with_template(position, template_coordinates, direction):
    
    
    # android_screen_x=1080
    # android_screen_y=1776
    # ios_screen_x=1242
    # ios_screen_y=2688
    
    # android_screen_x=1080
    # android_screen_y=2028
    # ios_screen_x=750
    # ios_screen_y=1334
      
    # The size has been moved to the top (global variables)

    android_screen_x=p_android_screen_x
    android_screen_y=p_android_screen_y
    ios_screen_x=p_ios_screen_x
    ios_screen_y=p_ios_screen_y
   
    if direction == 1:
        source_screen_x = android_screen_x
        source_screen_y = android_screen_y
        dest_screen_x = ios_screen_x
        dest_screen_y = ios_screen_y
    elif direction == 2:
        source_screen_x = ios_screen_x
        source_screen_y = ios_screen_y
        dest_screen_x = android_screen_x
        dest_screen_y = android_screen_y

    top_left_x = float(position[0])

    top_left_y = float(position[1])

    bottom_right_x = float(position[2])
    bottom_right_y = float(position[3])
    middle_x = (top_left_x+bottom_right_x)/2
    middle_y = (top_left_y+bottom_right_y)/2
    template_x = float(template_coordinates[0])
    template_y = float(template_coordinates[1])
    scaled_top_left_x = middle_x / dest_screen_x
    scaled_top_left_y = middle_y / dest_screen_y

    template_bottom_right_x = float(template_coordinates[2])
    template_bottom_right_y = float(template_coordinates[3])
    template_middle_x = (template_x+template_bottom_right_x)/2
    template_middle_y = (template_bottom_right_y+template_y)/2
    scaled_template_x = template_middle_x/source_screen_x

    scaled_template_y = template_middle_y / source_screen_y

    # template_x = float(args["x"])
    # template_y = float(args["y"])
    #return ((template_x - top_left_x)**2) + ((template_y - top_left_y)**2)
    return math.sqrt((scaled_template_x - scaled_top_left_x)**2) + ((scaled_template_y - scaled_top_left_y)**2)


def calc_score(source_widget_path, dest_widget_path, direction):
    lowe_ratio = 0.8
    orb = cv2.ORB_create()
    # bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # Read template image file and convert it to bw
    print("-----------------")
    print(dest_widget_path)
    print("-----------------")
    template = cv2.imread(source_widget_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Invert the template if it has dark background
    if dark_background(source_widget_path):
        template = cv2.bitwise_not(template)

    # template = cv2.Canny(template, 50, 200)
    template = cv2.GaussianBlur(template, (5, 5), cv2.BORDER_DEFAULT)
    image_text = None
    (tH, tW) = template.shape[:2]
    # plt.imshow(template, 'gray'), plt.show()

    template_text = OCR(source_widget_path, tH, tW)
    template_text = re.sub(r"([0-9 :]+(\.[0-9 :]+)?)", r" \1 ", template_text).strip()
    img3 = None

    if template_text:
        template_text = template_text.lower()
        template_words = set(template_text.split())

    template_coordinates = extract_position(source_widget_path)
    template_size = calc_image_size(source_widget_path)

    keypoints_1, descriptors_1 = orb.detectAndCompute(template, None)
    if descriptors_1 is None:
        image_similarity_score = 0

    #Up to this point we found descriptors and text inside source

    exact_text_match = False
    common_words = -1
    edit_distance = -1
    distance_score = 0
    key_point_score = 0
    size_similarity_score = 0
    proximity_score = 0

    image = cv2.imread(dest_widget_path)

    image_text = OCR(dest_widget_path, image.shape[0], image.shape[1])
    image_text = re.sub(r"([0-9 :]+(\.[0-9 :]+)?)", r" \1 ", image_text).strip()
    if image_text:
        print("image has text:" + image_text)

    if template_text:
        print("template has text:"+ template_text)
        if image_text:
            image_text = image_text.lower()
            if image_text == template_text:
                print("exact match: "+image_text)
                exact_text_match = True
                destance_score = 1
            else:
                image_words = set(image_text.split())
                common = template_words & image_words
                common_words = len(common)
                edit_distance = editdistance.eval(image_text,template_text)
                distance_score = 1 - edit_distance/max(len(image_text),len(template_text))

    if dark_background(dest_widget_path):
        print("here")
        # plt.imshow(image), plt.show()
        image = cv2.bitwise_not(image)
        # plt.imshow(image), plt.show()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.Canny(image, 50, 200)
    image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    (iH, iW) = image.shape[:2]

    keypoints_2, descriptors_2 = orb.detectAndCompute(image, None)

    if descriptors_2 is None or descriptors_1 is None:
        image_similarity_score = 0
    else:
        # matches = bf.match(descriptors_1, descriptors_2)
        matches = bf.knnMatch(descriptors_1, descriptors_2, k=2)

        # matches = sorted(matches, key=lambda x: x.distance)
        # for match in matches:
        #     key_point_score = key_point_score + match.distance



        # img3 = cv2.drawMatches(template, keypoints_1, image, keypoints_2, matches[:5], image, flags=2)
        # print(type(img3))
        # plt.imshow(img3),plt.show()
        #
        # print(key_point_score)

        good = []


        # print(matches)

        for i, pair in enumerate(matches):
            try:
                m, n = pair
                if m.distance < lowe_ratio * n.distance:
                    good.append([m])
            except ValueError:
                pass

        msg1 = 'using %s with lowe_ratio %.2f' % ('ORB', lowe_ratio)
        msg2 = 'there are %d good matches' % (len(good))


        img3 = cv2.drawMatchesKnn(template, keypoints_1, image, keypoints_2, good, None, flags=2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img3, msg1, (10, 250), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img3, msg2, (10, 270), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        fname = 'output_%s_%.2f.png' % ('ORB', lowe_ratio)
        cv2.imwrite(fname, img3)
        # if (len(good) > 0):
        #     plt.imshow(img3), plt.show()

        image_similarity_score = len(good)/max(len(descriptors_1),len(descriptors_2))
        print("image_similarity_score:")
        print(image_similarity_score)

    position = extract_position(dest_widget_path)
    size = calc_image_size(dest_widget_path)
    proximity_score = 1 - (find_distance_with_template(position, template_coordinates, direction) / math.sqrt(2))
    # android_size = 1080 * 1776
    # ios_size = 1242 * 2688
    # android_screen_x=1080
    # android_screen_y=1776
    # ios_screen_x=1242
    # ios_screen_y=2688



    # android_screen_x=1080
    # android_screen_y=2028
    # ios_screen_x=750
    # ios_screen_y=1334

    # The size has been moved to the top (global variables)

    android_screen_x=p_android_screen_x
    android_screen_y=p_android_screen_y
    ios_screen_x=p_ios_screen_x
    ios_screen_y=p_ios_screen_y
    
    ios_size = ios_screen_x*ios_screen_y
    android_size = android_screen_x* android_screen_y

    if direction == 1:
        source_size = android_size
        dest_size = ios_size
    else:
        source_size = ios_size
        dest_size = android_size

    size_similarity_score = 1 - abs(size / dest_size - template_size / source_size)
    return exact_text_match, common_words, proximity_score, size_similarity_score, image_similarity_score, distance_score, image_text, template_text, img3

