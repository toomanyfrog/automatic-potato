import os
import sys
from renameFiles import *

# python acceptCameraImgs.py mediaId

genpath = os.getcwd() + "/user/generated/" + sys.argv[1]
print "genpath: ", genpath
genfiles = os.listdir(genpath)
print genfiles, len(genfiles)

campath = os.getcwd() + "/user/camera/" + sys.argv[1]
print "campath: ", campath
camfiles = os.listdir(campath)
print camfiles, len(camfiles)


if len(genfiles) != len(camfiles):
    raise ValueError('did not upload correct amount of files')
