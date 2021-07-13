import argparse
import keypoint_comparator

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="platform A widget")
ap.add_argument("-i", "--images", required=True, help="platform B pngs")
args = vars(ap.parse_args())

keypoint_comparator.find_matching_widget(args["template"], args["images"])

