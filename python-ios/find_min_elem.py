import re

from appium import webdriver
from lxml import etree as ET

desired_caps = {
        "platformName": "iOS",
        "platformVersion": "13.4.1",
        "deviceName": "Someone's iPhone",
        "udid": "auto",
        "xcodeOrgId": "F9YGX7YPBF",
        "xcodeSigningId": "iPhone Developer"
}



def isElementInside(ele_x , ele_y, node):
        if ele_x==None or ele_y==None or node ==None:
            return False
        if "width" in node.attrib:
            if (int(node.attrib["x"])<= ele_x <=int(node.attrib["x"])+int(node.attrib["width"]))and (int(node.attrib["y"])<= ele_y <=int(node.attrib["y"])+int(node.attrib["height"])):
                return True, int(node.attrib["width"])*int(node.attrib["height"])
        elif "bounds" in node.attrib:
            boundStr=node.attrib['bounds']
                # if numOfChildren==0:
            if boundStr!=None:
                pattern=re.compile(r"\[(?P<x1>[\d]+),(?P<y1>[\d]+)]\[(?P<x2>[\d]+),(?P<y2>[\d]+)]")
                match = pattern.match(boundStr)
                if match:
                    x = int(match.group('x1'))
                    y = int(match.group('y1'))
                    x2 = int(match.group('x2'))
                    y2 =  int(match.group('y2'))
                    width = x2-x
                    height = y2-y
                    if (x <= ele_x <=x+width) and (y<= ele_y <=y+height):
                        return True, width*height
            else:
                print(str.format("Node: {} has no boundary, skipped",node.tag))
        return False,None

def findMinElement(ele_x,ele_y):
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    # print(driver.page_source)
    # str = open('python-ios/xmltest.txt', 'r').read()
    utf8_parser = ET.XMLParser(encoding='utf-8')
    root = ET.fromstring(driver.page_source.encode('utf-8'), parser=utf8_parser)
    tree = ET.ElementTree(root)
    dic={}
    minElement=None
    for child in root.iter():
        if not 'visible' in child.attrib:
            continue
        numOfChildren=len(child)
        if numOfChildren==0:
            #print(child.tag, child.attrib)
            #print(tree.getpath(child))
            isinside,size=isElementInside(ele_x,ele_y,child)
            if isinside:
                dic[child]=size
    temp = min(dic.values()) 
    res = [key for key in dic if dic[key] == temp] 
    minElement=res.pop()
    print("The enclosing element is:")
    # printing result  
    print(minElement)
    print(tree.getpath(minElement)) 
    # print(node)
    return minElement


if __name__ == "__main__":
    findMinElement(279,39)
    pass
