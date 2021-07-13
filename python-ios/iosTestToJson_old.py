from sys import argv
import re
import json

commentRegex = re.compile('#.*')
accessibilityIdRegex = re.compile('Click Element {4}accessibility id=(.*)')
idRegex = re.compile('Click Element {4}id=(.*)')
xPathRegex = re.compile('Click Element {4}xpath=(.*)')
absCoordsRegex = re.compile('Tap {4}accessibility id=composeButton\s+(\S*)\s+(\S*)')
inputTextByAccessibilityIdRegex = re.compile('Input Text    accessibility id=(\S+) {4}(.*)')

with open(argv[1], "r") as f:
    events = []
    for line in f.readlines():
        if commentRegex.match(line):
            # print("Comment Line!")
            continue

        match = accessibilityIdRegex.match(line)
        if match:
            event = {}
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
            event = {}
            event["type"] = "accessibilityId"
            event["event"] = "send_keys"
            event["tag"] = match.group(1)
            event["input"] = match.group(2)
            events.append(event)
            # print("Abs click on:", match.group(1), match.group(2))
            continue
            

        print("ERROR! Not supported event: ", line)

    res = {}
    res["events"] = events
    output = json.dumps(events, sort_keys=True, indent=4)
    # with open(argv[2], "w") as fw:
    #     fw.write(output)
    print(output)