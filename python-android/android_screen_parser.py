import pycurl
from io import BytesIO
import json
import xml.etree.ElementTree as ET
from queue import Queue

b_obj = BytesIO()
crl = pycurl.Curl()

# Set URL value
crl.setopt(crl.URL, 'http://127.0.0.1:8100/session/890CD0EE-EADA-4D3F-A74B-50AD2569E222/source')

# Write bytes that are utf-8 encoded
crl.setopt(crl.WRITEDATA, b_obj)

# Perform a file transfer 
crl.perform()

# End curl session
crl.close()

# Get the content stored in the BytesIO object (in byte characters) 
get_body = b_obj.getvalue()

# Decode the bytes stored in get_body to HTML and print the result 
res = json.loads(get_body.decode("utf8").strip())
print(res["value"])
root = ET.fromstring(res["value"])
counter = 0
f = open("settings.txt", "w")
f.write("digraph L {\n\n\tnode [shape=record fontname=Arial];\n\n")
queue = Queue()
queue.put(root)
parent = {}
numbering = {}
numInParent = {}
ordering = ""

while not queue.empty():
    node = queue.get()
    # print(node.attrib)
    numOfChildren = len(list(node))

    info = "{"
    for key, value in node.attrib.items():
        if key != "type":
            info += "|"
        info += key + " = " + value + "\\l"
    info += "|numberOfChildren = " + str(numOfChildren) + "\\l"
    if node in numInParent:
        info += "|numInParentLayout = " + str(numInParent[node]) + "\\l"
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
        if child.attrib["displayed"] == "true":
            queue.put(child)
            numInParent[child] = i
        i += 1
f.write("\n\n")
f.write(ordering)
f.write("\n\n}")
f.close()

# for child in root:
#     print(child.attrib)
#     print("\t", child.getchildren())
# print('Output of GET request:\n%s' % get_body.decode('utf8').strip())


