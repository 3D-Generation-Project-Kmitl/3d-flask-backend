import json
import math
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
    print('GPU Memory free',GPUtil.getGPUs()[0].memoryFree, file=sys.stderr)
    return GPUtil.getGPUs()[0].memoryFree < GPU_MEMORY_THRESHOLD
def waitWhenGPUMemoryLow():
    while x:
        x=isGPUMemoryLow()
        time.sleep(5)
def saveTransformJson(camera_data,transforms_file_path,images_path):
    print('type(camera_data)',type(camera_data))
    second_parameter=camera_data[1]['camera_parameter']
    img = cv2.imread(f'{images_path}/0001.jpg')
    h=float(img.shape[1])
    w=float(img.shape[0])
    # w = second_parameter['imageWidth']
    # h = second_parameter['imageHeight']

    fl_x = second_parameter['focalLength'][0]
    fl_y = second_parameter['focalLength'][1]
    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    p1 = second_parameter['focalLength'][0]
    p2 = second_parameter['focalLength'][1]
    cx = w / 2
    cy = h / 2
    angle_x = math.atan(w / (fl_x * 2)) * 2
    angle_y = math.atan(h / (fl_y * 2)) * 2
    fovx = angle_x * 180 / math.pi
    fovy = angle_y * 180 / math.pi
    out = {
			"camera_angle_x": angle_x,
			"camera_angle_y": angle_y,
			"fl_x": fl_x,
			"fl_y": fl_y,
			"k1": k1,
			"k2": k2,
			"k3": k3,
			"k4": k4,
			"p1": p1,
			"p2": p2,
            "is_fisheye": False,
			"cx": cx,
			"cy": cy,
			"w": w,
			"h": h,
			"aabb_scale": 4,
			"frames": [],
		}
    for cam in camera_data:
        print('cam',cam['camera_parameter'])
        frame = {"file_path":cam['file_path'],"transform_matrix": cam['camera_parameter']['cameraPose']} 
        out['frames'].append(frame)
    with open(transforms_file_path, "w") as outfile:
	    json.dump(out, outfile, indent=2)
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
    
def unZipImages(image_zip_path,images_path):
    with ZipFile(image_zip_path,'r') as zObject:
        if os.path.exists(images_path):
            do_system(f'rm {images_path} -r')
        os.mkdir(images_path)
        zObject.extractall(path=images_path)

def constructTransformsJson():
     pass




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