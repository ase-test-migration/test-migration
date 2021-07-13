import json
import os
import sys

from appium import webdriver

import layout_tree


class DynElementExtractor:

    def __init__(self, elementPathToMatch):
        with open(os.path.join(sys.path[0],"dev_info.json")) as f:
            metadata = json.load(f)
        desiredCapabilities = metadata["desiredCapabilities"]
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desiredCapabilities)
        assert driver != None
        self.driver = driver
        self.elementPathToMatch=[]
        self.elementPathToMatch.append(elementPathToMatch)

    def createDir(self, name):
        import os
        try:
            os.rmdir(name)
        except:
            print("{} Not exists.".format(name))
            pass
        try:
            os.mkdir(name)
        except:
            print("{} failed!.".format(name))
            pass
    
    def runFind(self):
        i = 0
        #print(self.driver.page_source)
        for elemPath in self.elementPathToMatch:
            stateNamePath = "S{}".format(i)
            self.createDir(stateNamePath)
            #elem= self.driver.find_element_by_image(elemPath)
            layoutTree = layout_tree.LayoutTree(self.driver, stateNamePath)
            elem=layoutTree.findElementByImagePath(elemPath)
            
            

            # pathToElementImage, bounds = self.execEvent(event, stateNamePath)
            # with open("{}/event_metadata.txt".format(stateNamePath), "w") as f:
            #     f.write("pathToElementImageCrop: {};\n".format(pathToElementImage))
            #     f.write("coords: {};\n".format(bounds))
            i += 1

if __name__ == "__main__":
    s = DynElementExtractor("python-ios/tests/testSubwayBtmMenu/S0/pngs/4.0_1238.0_146.0_1334.0.png")
    s.runFind()