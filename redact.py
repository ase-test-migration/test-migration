# Python program to extract text from all the images in a folder
# storing the text in corresponding files in a different folder
from PIL import Image
import pytesseract as pt
import os
import glob, os
from pathlib import Path
from multiprocessing import Pool, Manager
from shutil import copy2
from send2trash import send2trash
directory='./privacy_to_delete'
def checkRedact(img_path):
    private_list = [''] # sample :['gmail.com','someschool.edu']
    # print(img_path)
    img = Image.open(img_path)
    print("Searching: {}".format(img_path),end="\r")
    # applying ocr using pytesseract for python
    text = pt.image_to_string(img, lang ="eng")
    #print(text)
    matched_content=[]
    for ele in private_list:
        if ele in text:
            matched_content.append(ele)
        
    if len(matched_content)>0:
        print("Matched {} in:{}".format(matched_content,img_path),flush=True)
        file1 = open("file_to_redact.txt", "a")  # append mode
        file1.write(str(img_path)+"\n")
        file1.close()
        # copy to privacy folder for inspection.
        # copy2(img_path, directory)

        # dangerous, send to trash, remember to clean your recycle bin first.
        # pip install send2trash
        # send2trash(str(img_path))
        

if __name__ =='__main__':
    image_list=Path('./').rglob('*.png')
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        files = glob.glob(directory+'/*')
        for f in files:
            os.remove(f)
    p=Pool()
    with p:
        p.map(checkRedact,image_list)
