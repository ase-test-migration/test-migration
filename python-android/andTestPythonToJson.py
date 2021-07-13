from sys import argv
import re
import json
import os

# Syntax: iosTestToJson.py app_abbr test_name
# generate cases like test_ios_xxxx_1.json
# Set your android/ios property here
# choose android/ios
platformName = "Android"

# properties on both platform
deviceName = "emulator-5554"  # "Someone's iPhone"

# ios only
platformVersion = "13.3.1"

udid = "auto"
xcodeOrgId = "X9EN5J4J22"
xcodeSigningId = "iPhone Developer"

# set to False if you do not want it to save to a file.
writeToFile = True

find_line_regex = re.compile('.*driver.find_element_by_(.*)\(\"(.*)\"\)')
action_line_regex = re.compile('el.*\.(.*)\((.*)\)')

with open("testcase_src", "r") as f:
    events = []
    for find_line in f:
        action_line = next(f, None)

        find_line_info = find_line_regex.match(find_line)
        event_type = find_line_info.group(1)
        event_tag = bytes(find_line_info.group(2), "utf-8").decode("unicode_escape")

        action_line_info = action_line_regex.match(action_line)
        event_event = action_line_info.group(1)
        event_input = bytes(action_line_info.group(2), "utf-8").decode("unicode_escape")

        event = {}
        if event_type == "accessibility_id":
            event["type"] = "accessibilityId"
        elif event_type == "xpath":
            event["type"] = "xPath"
        elif event_type == "id":
            event["type"] = "id"
        # TODO: Add support for finding element by coordinates
        else:
            print("Unknown event type. Skipping test step...")
            continue

        event["event"] = event_event
        event["tag"] = event_tag

        if event_event == "send_keys":
            event["input"] = event_input[1:-1]

        events.append(event)

app_abbr = argv[1]
testname = argv[2]
if not testname:
    raise Exception("Sorry, plesase input testname")
if not app_abbr:
    raise Exception("Sorry, plesase input app_abbr")
res = {}
res["name"] = app_abbr + "-" + testname
res["events"] = events
tests = []
tests.append(res)
dc = {}

document = {}
if platformName == "Android":
    dc["platformName"] = platformName
    dc["deviceName"] = deviceName
    dc["newCommandTimeout"] = 0

else:
    dc["platformName"] = platformName
    dc["platformVersion"] = platformVersion
    dc["deviceName"] = deviceName
    dc["udid"] = udid
    dc["xcodeOrgId"] = xcodeOrgId
    dc["xcodeSigningId"] = xcodeSigningId

document["desiredCapabilities"] = dc

document["tests"] = tests

output = json.dumps(document, sort_keys=False, indent=4)
i = 1
filename = "test_{}_{}_{}.json".format(platformName.lower(), app_abbr, str(i))
while os.path.exists(filename):
    i += 1
    filename = "test_{}_{}_{}.json".format(platformName.lower(), app_abbr, str(i))
print(output)
if writeToFile:
    with open(filename, "w") as fw:
        fw.write(output)
        print("Writing to {}....".format(filename))
