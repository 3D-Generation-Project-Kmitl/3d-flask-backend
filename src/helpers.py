import os,sys
import re
import time
import cv2
from zipfile import ZipFile
import GPUtil
from constants import *
import numpy as np
import pyrender
import trimesh

def isGPUMemoryLow():
    print('GPU Memory free',GPUtil.getGPUs()[0].memoryFree)
    return GPUtil.getGPUs()[0].memoryFree < GPU_MEMORY_THRESHOLD
def waitWhenGPUMemoryLow():
    while isGPUMemoryLow():
        time.sleep(5)
def renderAndSave3DIn2DImages(mesh_path,image_path):

    model = trimesh.load(mesh_path)
    mesh = pyrender.Mesh.from_trimesh(model, smooth=False)


    scene = pyrender.Scene(ambient_light=[.1, .1, .3], bg_color=[0, 0, 0])
    camera = pyrender.PerspectiveCamera( yfov=np.pi / 3.0)
    light = pyrender.DirectionalLight(color=[1,1,1], intensity=2e3)

    scene.add(mesh, pose=  np.eye(4))
    scene.add(light, pose=  np.eye(4))

    c = 2**-0.5
    scene.add(camera, pose=[[ 1,  0,  0,  0],
                            [ 0,  c, -c, -2],
                            [ 0,  c,  c,  2],
                            [ 0,  0,  0,  1]])

    r = pyrender.OffscreenRenderer(512, 512)
    color, _ = r.render(scene)
    cv2.imwrite(image_path,color)

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