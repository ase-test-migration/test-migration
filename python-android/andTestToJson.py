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

commentRegex = re.compile('#.*')
accessibilityIdRegex = re.compile('Click Element {4}accessibility id=(.*)')
idRegex = re.compile('Click Element {4}id=(.*)')
xPathRegex = re.compile('Click Element {4}xpath=(.*)')
absCoordsRegex = re.compile('Tap {4}accessibility id=composeButton\s+(\S*)\s+(\S*)')
inputTextByAccessibilityIdRegex = re.compile('Input Text {4}accessibility id=(.*) {4}(.*)')
inputTextByIdRegex = re.compile('Input Text {4}id=(\S+) {4}(.*)')
inputTextByxPathRegex = re.compile('Input Text {4}xpath=(.*) {4}(.*)')
backRegex = re.compile('Go Back')

with open("testcase_src", "r") as f:
    events = []
    for line in f.readlines():
        if commentRegex.match(line):
            # print("Comment Line!")
            continue

        match = accessibilityIdRegex.match(line)
        if match:
            event = {}
            print("here")
            event["type"] = "accessibilityId"
            event["event"] = "click"
            event["tag"] = match.group(1)
            events.append(event)
            # print("A11y click on:", match.group(1))
            continue

        match = idRegex.match(line)
        if match:
            event = {}
            event["type"] = "id"
            event["event"] = "click"
            event["tag"] = match.group(1)
            events.append(event)
            # print("A11y click on:", match.group(1))
            continue

        match = xPathRegex.match(line)
        if match:
            event = {}
            event["type"] = "xPath"
            event["event"] = "click"
            event["tag"] = match.group(1)
            events.append(event)
            # print("xPath click on:", match.group(1))
            continue

        match = absCoordsRegex.match(line)
        if match:
            event = {}
            event["type"] = "coordinate"
            event["event"] = "click"
            event["x"] = match.group(1)
            event["y"] = match.group(2)
            events.append(event)
            # print("Abs click on:", match.group(1), match.group(2))
            continue

        match = inputTextByAccessibilityIdRegex.match(line)
        if match:
            print("here")
            event = {}
            event["type"] = "accessibilityId"
            event["event"] = "send_keys"
            event["tag"] = match.group(1)
            event["input"] = match.group(2)
            events.append(event)
            # print("Abs click on:", match.group(1), match.group(2))
            continue

        match = inputTextByIdRegex.match(line)
        if match:
            event = {}
            event["type"] = "id"
            event["event"] = "send_keys"
            event["tag"] = match.group(1)
            event["input"] = match.group(2)
            events.append(event)
            # print("Abs click on:", match.group(1), match.group(2))
            continue

        match = inputTextByxPathRegex.match(line)
        if match:
            event = {}
            event["type"] = "xPath"
            event["event"] = "send_keys"
            event["tag"] = match.group(1)
            event["input"] = match.group(2)
            events.append(event)
            # print("Abs click on:", match.group(1), match.group(2))
            continue

        match = backRegex.match(line)
        if match:
            event = {}
            event["event"] = "back"
            events.append(event)
            continue

        print("ERROR! Not supported event: ", line)

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
