import os
import sys
from renameFiles import *

# python acceptCameraImgs.py mediaId

genpath = os.getcwd() + "/user/generated/" + sys.argv[1]
genfiles = os.listdir(genpath)

campath = os.getcwd() + "/user/camera/" + sys.argv[1]
camfiles = os.listdir(campath)

if len(genfiles) != len(camfiles):
    raise ValueError('did not upload correct amount of files')
