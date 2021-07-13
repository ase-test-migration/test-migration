# extract the element and locate it from the dot file.
import argparse
import os
import re
from collections import defaultdict


def find_path(graph, start, end, path=None):
    if path is None:
        path = []
    path += [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None


def findXPath(inputImagePath, dotPath):
    # dotPath="python-android/testAOLVideo/S0/graph.dot"
    # inputImagePath="python-android/testAOLVideo/S0/pngs/30_372_1050_522.png"
    linenum = r"^\t(\d+)\s+\["
    lineregex = re.compile(linenum)
    dotRegex = re.compile(r"^\t(\d+) -> (\d+)")
    matchedList = []
    with open(dotPath) as search:
        for line in search:
            if os.path.basename(inputImagePath) in line:
                # print(line)
                match = lineregex.match(line)
                if match:
                    linenum = int(match.group(1))
                    # print(linenum)
                    matchedList.append(int(linenum))
    print("The list is:{}".format(matchedList))
    maxlinenum = max(matchedList)
    print("The max line number is:{}".format(maxlinenum))

    dic = defaultdict(list)

    with open(dotPath) as search:
        for line in search:
            match = dotRegex.match(line)
            # print(line)
            if match:
                parent = str(match.group(1))
                child = str(match.group(2))

                dic[parent].append(child)

                # if len(sys.argv)==1:
    print(dic)

    contentRegex = re.compile(r"\|(.+) = (.*)")
    path = find_path(dic, str(0), str(maxlinenum))

    print("The path is:{}".format(path))
    trans = re.compile(r"\[label=\"(.+)\"]")

    jsonlist = []
    for elem in path:
        with open(dotPath) as search:
            for line in search:
                if re.search(rf"^\t{elem}\s+\[", line):
                    # print(line)
                    match = trans.search(line)
                    json = {}
                    if match:
                        content = match.group(1).replace('\\l', '\n').replace('}', '').replace('{', '|')
                        # print(content)
                        for sline in content.splitlines():
                            mat = contentRegex.search(sline)
                            if mat:
                                json[mat.group(1)] = mat.group(2)
                        # print(json)
                        jsonlist.append(json)

    xpath = ""
    first = True
    for elem in jsonlist:
        # print(elem["class"])

        if first:
            first = False
            prev_num_of_children = 1
        if "numInParentLayout" in elem:
            if int(prev_num_of_children) != 1:
                xpath += "/{}[{}]".format(elem["type"], str(int(elem["numInParentLayout"]) + 1))
            else:
                xpath += "/{}".format(elem["type"])
        else:
            xpath += "/{}".format(elem["type"])
        prev_num_of_children = elem["numberOfChildren"]

    print(xpath)
    print("end of xpath")
    return xpath, jsonlist


if __name__ == "__main__":
    # image path, dotpath
    # findXPath(sys.argv[1],sys.argv[2])
    parser = argparse.ArgumentParser(description="Given an cropped element path, Find element\'s xPath in the layout "
                                                 "from existing dot file ")
    parser.add_argument('inputImagePath', action="store")
    parser.add_argument('dotPath', action="store")
    args = parser.parse_args()
    findXPath(args.inputImagePath, args.dotPath)
    pass
