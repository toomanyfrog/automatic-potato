import shutil
import os


#TODO: generalise the filepath for all user-submitted folders
path =  os.getcwd() + "/images/user/3e35/"
filenames = os.listdir(path)

print path
print filenames

for i in range(len(filenames)):
    if filenames[i][0] != '.':
        shutil.move(path+filenames[i], path+str(i) + ".jpg")
