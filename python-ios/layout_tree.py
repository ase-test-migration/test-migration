import xml.etree.ElementTree as ET
from queue import Queue 
from PIL import Image
from io import BytesIO 
from sys import argv
import base64
import os
from lxml import etree
import re
import node
import state

class LayoutTree:
    
    def __init__(self, driver, pathName):
        self.pagesrc=driver.page_source
        self.root = ET.fromstring(driver.page_source)
        print(self.root)
        self.pathName = pathName        
        try:
            import os
            os.mkdir("{}/pngs".format(pathName))
        except:
            print("FAILED TO CREATE PNGS!")

        # self.createDirs()

        data = base64.decodebytes(driver.get_screenshot_as_base64().encode())
        self.screenshot = Image.open(BytesIO(data))
        self.screenshotWidth, self.screenshotHeight = self.screenshot.size
        # print(self.width, self.height)
    
    def createDirs(self):
        from shutil import rmtree
        path = "./{}/{}/pngs".format(self.appName, self.stateName)
        try:
            rmtree(path)
        except:
            print("Failed to remove tree. Prob not existing")

        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

    def androidBoundtransform(self, boundStr):
        # if numOfChildren==0:
        if boundStr!=None:
            pattern=re.compile(r"\[(?P<x1>[\d]+),(?P<y1>[\d]+)]\[(?P<x2>[\d]+),(?P<y2>[\d]+)]")
            match = pattern.match(boundStr)
            if match:
                x = int(match.group('x1'))
                y = int(match.group('y1'))
                x2 =  match.group('x2')
                y2 =  match.group('y2')
                width = int(match.group('x2'))-int(match.group('x1'))
                height = int(match.group('y2'))-int(match.group('y1'))
                print("X:{}\nY:{}\nX2:{}\nY2:{}\nWidth:{}\nHeight:{}\n".format(x,y,x2,y2,width,height))
        return x, y, width, height

    def saveCroppedImage(self, x, y, width, height):
        actualX = float(x) / self.scaleWidth
        actualX *= self.screenshotWidth
        
        actualY = float(y) / self.scaleHeigh
        actualY *= self.screenshotHeight

        actualWidth = float(width) / self.scaleWidth
        actualWidth *= self.screenshotWidth

        actualHeight = float(height) / self.scaleHeigh
        actualHeight *= self.screenshotHeight

        x1 = actualX
        y1 = actualY
        x2 = actualX + actualWidth
        y2 = actualY + actualHeight

        print(x1, y1, x2, y2)

        b = (x1, y1, x2, y2)
        cropSuffix = str(actualX) + "_" + str(actualY) + "_" + str(actualX + actualWidth) + "_" + str(actualY + actualHeight)
        
        crop = self.screenshot.crop(box=b)
        name = "{}/pngs/{}.png".format(self.pathName, cropSuffix)
        crop.save(name)
        crop = crop.convert('L')
        # crop = crop.convert('1')
        # crop.save("{}/pngs/{}_bw.png".format(self.pathName, cropSuffix))
        bounds = {}
        bounds["x1"] = x1
        bounds["y1"] = y1
        bounds["x2"] = x2
        bounds["y2"] = y2
        return name, bounds

    def isElementInside(self, ele_x , ele_y, node):
        if ele_x==None or ele_y==None or node ==None:
            return False
        if "width" in node.attrib:
            #TODO: We might have crash problems with this on some webapp based apps! Sample: IKEA_1
            if (int(node.attrib["x"])<= int(ele_x) <=int(node.attrib["x"])+int(node.attrib["width"]))and (int(node.attrib["y"])<= int(ele_y) <=int(node.attrib["y"])+int(node.attrib["height"])):
                return True, int(node.attrib["width"]) * int(node.attrib["height"])
        elif "bounds" in node.attrib:
            boundStr=node.attrib['bounds']
                # if numOfChildren==0:
            if boundStr!=None:
                x, y, width, height=self.androidBoundtransform(boundStr)
                if (x <= ele_x <=x+width) and (y<= ele_y <=y+height):
                    return True, width * height
            else:
                print(str.format("Node: {} has no boundary, skipped",node.tag))
        return False,None

    def isElementMatching(self, saveElementBoundsRect, node):
        if saveElementBoundsRect == None:
            return False
        if (int(saveElementBoundsRect["width"]) == int(node.attrib["width"]) and saveElementBoundsRect["height"] == int(node.attrib["height"]) and saveElementBoundsRect["x"] == int(node.attrib["x"]) and saveElementBoundsRect["y"] == int(node.attrib["y"])):
            return True
        return False

    def findElementByImagePath(self, imagePath):
        # im=Image.open(imagePath)
        # width, height=im.size

        x1=x2=y1=y2=0
        filename=os.path.basename(imagePath)
        #x1) + "_" + str(y1) + "_" + str(x2) + "_" + str(actualY + actualHeight
        #  
        boundRegex=re.compile(r"(\d+\.?\d*)_(\d+\.?\d*)_(\d+\.?\d*)_(\d+\.?\d*).png")
        match = boundRegex.match(filename)
        if match:
            f_x1=int(float(match.group(1)))
            f_y1=int(float(match.group(2)))
            f_x2=int(float(match.group(3)))
            f_y2=int(float(match.group(4)))

        # print(driver.page_source)
        # str = open('python-ios/xmltest.txt', 'r').read()
        utf8_parser = etree.XMLParser(encoding='utf-8')
        root = etree.fromstring(self.pagesrc.encode('utf-8'), parser=utf8_parser)
        tree = etree.ElementTree(root)
        dic={}
        bound={}
        for child in root.iter():
            if child.tag == 'XCUIElementTypeApplication':
                self.scaleWidth = int(child.attrib["width"])
                self.scaleHeigh = int(child.attrib["height"])
                print(self.scaleWidth, self.scaleHeigh)
            if not 'visible' in child.attrib:
                continue
            numOfChildren=len(child)
            if child.attrib['visible']=='true':
                #print(child.tag, child.attrib)
                #print(tree.getpath(child))
                x1 = f_x1 * self.scaleWidth / self.screenshotWidth
                y1 = f_y1 * self.scaleHeigh/ self.screenshotHeight 
            
                x2 = f_x2 * self.scaleWidth / self.screenshotWidth
                y2 = f_y2 * self.scaleHeigh / self.screenshotHeight  
                bound["width"]=x2-x1
                bound["height"]=y2-y1
                bound["x"]=x1
                bound["y"]=y1
                
                if self.isElementMatching(bound,child):
                    print("The matched element is:"+ tree.getpath(child))
                    dic[child]=numOfChildren
        
        temp = min(dic.values()) 
        res = [key for key in dic if dic[key] == temp] 
        minElement=res[0]
        print("The mininum matched child is:"+tree.getpath(minElement))

        return minElement

    def findMinElement(self,ele_x,ele_y):
        # print(driver.page_source)
        # str = open('python-ios/xmltest.txt', 'r').read()
        utf8_parser = etree.XMLParser(encoding='utf-8')
        root = etree.fromstring(self.pagesrc.encode('utf-8'), parser=utf8_parser)
        tree = etree.ElementTree(root)
        dic={}
        minElement=None
        for child in root.iter():
            if child.tag == 'XCUIElementTypeApplication':
                self.scaleWidth = float(child.attrib["width"])
                self.scaleHeigh = float(child.attrib["height"])
                print(self.scaleWidth, self.scaleHeigh)
            if not 'visible' in child.attrib:
                continue
            numOfChildren=len(child)
            if numOfChildren==0:
                #print(child.tag, child.attrib)
                #print(tree.getpath(child))
                isinside,size = self.isElementInside(ele_x,ele_y,child)
                if isinside:
                    dic[child]=size
        temp = min(dic.values()) 
        res = [key for key in dic if dic[key] == temp] 
        minElement=res.pop()
        print("The enclosing element is:")
        # printing result  
        print(tree.getpath(minElement)) 
        # print(node)s
        screenshotFileName, tmpBounds=self.saveCroppedImage(minElement.attrib["x"], minElement.attrib["y"], minElement.attrib["width"], minElement.attrib["height"])
        return screenshotFileName, tmpBounds

    def printTree(self, saveElementBoundsRect=None, saveCrops=True, onlyVisible=True):
        counter = 0
        f = open("{}/graph.dot".format(self.pathName), "w")
        textual_data_file = open("{}/texts.txt".format(self.pathName), "w")
        f.write("digraph Layout {\n\n\tnode [shape=record fontname=Arial];\n\n")
        queue = Queue()
        queue.put(self.root)
        parent = {}
        numbering = {}
        numInParent = {}
        ordering = ""

        pngToMatchedElementPath = None
        bounds = None
        matched_textual_info = ""
        while not queue.empty():
            node = queue.get()
            has_name = False
            print(node.tag)
            
            # Skip on AppiumAUT XML node, since I doesn't have useful info.
            if node.tag == 'AppiumAUT':
                for child in node:
                    queue.put(child)
                continue

            if node.tag == 'XCUIElementTypeApplication':
                self.scaleWidth = float(node.attrib["width"])
                self.scaleHeigh = float(node.attrib["height"])
                print(self.scaleWidth, self.scaleHeigh)

            numOfChildren = len(list(node))


            info = "{"
            for key, value in node.attrib.items():
                if key != "type":
                    info += "|"
                info += key + " = " + value + "\\l"

                if key == "name":
                    textual_info = "\"name\" : \"" +  value + "\""
                    if not has_name:
                        textual_data_file.write("{")
                    textual_data_file.write(textual_info+ ", ")
                    has_name = True

                if key == "label":
                    textual_info = "\"label\" : \"" + value + "\""
                    if not has_name:
                        textual_data_file.write("{")
                    textual_data_file.write(textual_info + ", ")
                    has_name = True

                if key == "value":
                    textual_info = "\"value\" : \"" + value + "\""
                    if not has_name:
                        textual_data_file.write("{")
                    textual_data_file.write(textual_info + ", ")
                    has_name = True

            info += "|numberOfChildren = " + str(numOfChildren) + "\\l"
            if node in numInParent:
                info += "|numInParentLayout = " + str(numInParent[node]) + "\\l" 
                   
            isElementMatched = self.isElementMatching(saveElementBoundsRect, node)
            if isElementMatched:
                info += "|eventGeneratedOnElement = true \\l"
            else:
                info += "|eventGeneratedOnElement = false \\l"

            if saveCrops and node.attrib["visible"] == "true" and not (node.attrib["width"] == 0 and node.attrib["height"] == 0):
                print("Saving crop!")
                screenshotFileName, tmpBounds = self.saveCroppedImage(node.attrib["x"], node.attrib["y"], node.attrib["width"], node.attrib["height"])
                if has_name:
                    textual_data_file.write("\"screenshotPath\" : \"" +  screenshotFileName + "\"}\n")
                    has_name = False
                info += "|screenshotPath = " + screenshotFileName + "\\l"
                if isElementMatched:
                    pngToMatchedElementPath = screenshotFileName
                    bounds = tmpBounds

            if isElementMatched:
                matched_textual_info = textual_info

            info += "}"
            # print(info)

            string = "\t" + str(counter) + "\t[label=\"" + info + "\"]\n"
            numbering[node] = counter
            f.write(string)

            if node in parent:
                ordering += "\t" + str(numbering[parent[node]]) + " -> " + str(counter) + "\n"
        
            counter += 1
            i = 0
            for child in node:
                parent[child] = node
                if not onlyVisible or child.attrib["visible"] == "true":
                    queue.put(child)
                    numInParent[child] = i
                i += 1
            
        f.write("\n\n")
        f.write(ordering)
        f.write("\n\n}")
        f.close()
        
        return pngToMatchedElementPath, bounds, matched_textual_info

    def saveScreenshot(self):
        self.screenshot.save("{}_whole.png".format(self.name))

    def extract_state(self, saveElementBoundsRect=None, saveCrops=True, onlyVisible=True):
        counter = 0
        f = open("{}/graph.dot".format(self.pathName), "w")
        f.write("digraph Layout {\n\n\tnode [shape=record fontname=Arial];\n\n")
        curr_state = state.State(self.screenshot)
        queue = Queue()
        queue.put(self.root)
        parent = {}
        numbering = {}
        numInParent = {}
        ordering = ""

        pngToMatchedElementPath = None
        bounds = None

        while not queue.empty():
            source_node = queue.get()
            print(source_node.tag)

            # Skip on AppiumAUT XML node, since I doesn't have useful info.
            if source_node.tag == 'AppiumAUT':
                for child in source_node:
                    queue.put(child)
                continue

            if source_node.tag == 'XCUIElementTypeApplication':
                self.scaleWidth = float(source_node.attrib["width"])
                self.scaleHeigh = float(source_node.attrib["height"])
                print(self.scaleWidth, self.scaleHeigh)

            numOfChildren = len(list(source_node))

            info = "{"
            for key, value in source_node.attrib.items():
                if key != "type":
                    info += "|"
                info += key + " = " + value + "\\l"

            info += "|numberOfChildren = " + str(numOfChildren) + "\\l"
            if source_node in numInParent:
                info += "|numInParentLayout = " + str(numInParent[source_node]) + "\\l"

            isElementMatched = self.isElementMatching(saveElementBoundsRect, source_node)
            if isElementMatched:
                info += "|eventGeneratedOnElement = true \\l"
            else:
                info += "|eventGeneratedOnElement = false \\l"

            if saveCrops and source_node.attrib["visible"] == "true" and not (
                    source_node.attrib["width"] == 0 and source_node.attrib["height"] == 0):
                print("Saving crop!")
                screenshotFileName, tmpBounds = self.saveCroppedImage(source_node.attrib["x"], source_node.attrib["y"],
                                                                      source_node.attrib["width"], source_node.attrib["height"])
                info += "|screenshotPath = " + screenshotFileName + "\\l"
                if isElementMatched:
                    pngToMatchedElementPath = screenshotFileName
                    bounds = tmpBounds


            curr_node = node.Node(counter, source_node.attrib, "iOS", None, numOfChildren, source_node.tag, screenshotFileName)
            info += "}"
            # print(info)

            string = "\t" + str(counter) + "\t[label=\"" + info + "\"]\n"
            numbering[source_node] = counter
            f.write(string)

            curr_state.add_node(curr_node)

            if source_node in parent:
                ordering += "\t" + str(numbering[parent[source_node]]) + " -> " + str(counter) + "\n"

            counter += 1
            i = 0
            for child in source_node:
                parent[child] = source_node
                if not onlyVisible or child.attrib["visible"] == "true":
                    queue.put(child)
                    numInParent[child] = i
                i += 1

        f.write("\n\n")
        f.write(ordering)
        f.write("\n\n}")
        f.close()

        return curr_state

if __name__=="__main__":
    import shutil

    path = "{}/{}/pngs".format("APP1", "S0")
    try:
        shutil.rmtree(path)
    except:
        print("Failed to removed dir. Not existing.")

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    # import unittest
    # from appium import webdriver
    
    # desired_caps = {
    #     'platformName' : 'iOS',
    #     'xcodeOrgId' : '5FLNFHR2L3',
    #     'automationName' : 'xcuitest',
    #     'deviceName' : 'Someone\'s iPhone',
    #     'udid' : 'bdf8ac24c06288f44ac43ebe32b2c23e6e49b7e2'
    # }

    # print(argv[1])
    # driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    # x = LayoutTree(driver, argv[1], argv[2])
    # x.printTree()
