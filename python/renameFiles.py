import shutil
import os


#TODO: generalise the filepath for all user-submitted folders
path =  os.getcwd() + "/4cp/"
filenames = os.listdir(path)

print path
print filenames

for i in range(len(filenames)):
    shutil.move(path+filenames[i], path+str(i) + ".jpg")
