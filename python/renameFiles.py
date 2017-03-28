import shutil
import os

def renameFiles(folderpath):
    path =  os.getcwd() + folderpath
    filenames = os.listdir(path)

    for i in range(len(filenames)):
        if filenames[i][0] != '.':
            shutil.move(path+filenames[i], path+str(i) + ".jpg")
