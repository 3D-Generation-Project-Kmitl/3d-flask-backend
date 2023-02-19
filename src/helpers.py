import os,sys
import re
import time
import cv2
from zipfile import ZipFile
import GPUtil
from constants import *

def isGPUMemoryLow():
    print('GPU Memory free',GPUtil.getGPUs()[0].memoryFree)
    return GPUtil.getGPUs()[0].memoryFree < GPU_MEMORY_THRESHOLD
def waitWhenGPUMemoryLow():
    while isGPUMemoryLow():
        time.sleep(5)
def getMarchingCubesRes(quality):
    if(quality=='High'):
        return HIGH_MARCHING_CUBES_RES
    elif(quality=='Medium'):
        return MEDIUM_MARCHING_CUBES_RES
    else:
        return LOW_MARCHING_CUBES_RES
def replaceWordInTransformsJson(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def unZipImages(imagesZipPath,images_path):
    with ZipFile(imagesZipPath,'r') as zObject:
        if os.path.exists(images_path):
            do_system(f'rm {images_path} -r')
        os.mkdir(images_path)
        zObject.extractall(path=images_path)

def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		# sys.exit(err)
# def getFPSForCOLMAP(video_path):
#     fps=128.0/getVideoDurationInSeconds(video_path)
#     if fps<2:
#         fps=2
#     return int(fps)
# def getVideoDurationInSeconds(video_path):
#     data = cv2.VideoCapture(video_path)
 
#     # count the number of frames
#     frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
#     fps = data.get(cv2.CAP_PROP_FPS)
 
#     # calculate duration of the video
#     seconds = round(frames / fps)
#     return seconds