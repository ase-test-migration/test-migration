from os.path import normpath, basename
index = 2
statepathname = "bbc-my-news/S10"
base = statepathname.split("/")[0]
print(base)
newstatepathname = base+"/S"+ str(index)
print(newstatepathname)