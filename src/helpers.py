import os,sys
import re
import cv2
from zipfile import ZipFile

def replaceWordInTransformsJson(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def getFPSForCOLMAP(video_path):
    fps=128.0/getVideoDurationInSeconds(video_path)
    if fps<2:
        fps=2
    return int(fps)
def getVideoDurationInSeconds(video_path):
    data = cv2.VideoCapture(video_path)
 
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
 
    # calculate duration of the video
    seconds = round(frames / fps)
    return seconds
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