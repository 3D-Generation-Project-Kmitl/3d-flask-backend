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
def rotmat(a, b):
	a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
	v = np.cross(a, b)
	c = np.dot(a, b)
	# handle exception for the opposite direction input
	if c < -1 + 1e-10:
		return rotmat(a + np.random.uniform(-1e-2, 1e-2, 3), b)
	s = np.linalg.norm(v)
	kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
	return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2 + 1e-10))

def closest_point_2_lines(oa, da, ob, db): # returns point closest to both rays of form o+t*d, and a weight factor that goes to 0 if the lines are parallel
	da = da / np.linalg.norm(da)
	db = db / np.linalg.norm(db)
	c = np.cross(da, db)
	denom = np.linalg.norm(c)**2
	t = ob - oa
	ta = np.linalg.det([t, db, c]) / (denom + 1e-10)
	tb = np.linalg.det([t, da, c]) / (denom + 1e-10)
	if ta > 0:
		ta = 0
	if tb > 0:
		tb = 0
	return (oa+ta*da+ob+tb*db) * 0.5, denom
def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()
def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm
     
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
    p1 = 0
    p2 = 0
    cx = second_parameter['principlePoint'][0]
    cy = second_parameter['principlePoint'][1]
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
    out2 = {
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
    up = np.zeros(3)
    for cam in camera_data:
        # print('cam',cam['camera_parameter'])
        print('pure',cam['camera_parameter']['cameraPose'], file=sys.stderr)
        print('phol',type(cam['camera_parameter']['cameraPose']), file=sys.stderr)
        
        print('camPse ',cam['camera_parameter']['cameraPose'])
        print('np array ',np.array(cam['camera_parameter']['cameraPose']))
        c2w = np.linalg.inv(cam['camera_parameter']['cameraPose'])
        # c2w=np.array(cam['camera_parameter']['cameraPose'])
        # c2w[0:3,2] *= -1 # flip the y and z axis
        # c2w[0:3,1] *= -1
        # c2w = c2w[[1,0,2,3],:]
        # c2w[2,:] *= -1 # flip whole world upside dow
        # up += c2w[0:3,1]
        # b = sharpness('./'+cam['file_path'])
        frame = {"file_path":cam['file_path'],"sharpness":100,"transform_matrix": c2w}
        # frame2 = {"file_path":cam['file_path'],"transform_matrix": cam['camera_parameter']['cameraPose']} 
        out['frames'].append(frame)
        # out2['frames'].append(frame2)
    flip_mat = np.array([
			[1, 0, 0, 0],
			[0, -1, 0, 0],
			[0, 0, -1, 0],
			[0, 0, 0, 1]
		])

    for f in out["frames"]:
        f["transform_matrix"] = np.matmul(f["transform_matrix"], flip_mat) # flip cameras (it just works)
    # nframes = len(out["frames"])
    # print("np.linalg.norm(up) was",np.linalg.norm(up))
    # up = up / np.linalg.norm(up)
    # print("up vector was", up)
    # R = rotmat(up,[0,0,1]) # rotate up vector to [0,0,1]
    # R = np.pad(R,[0,1])
    # R[-1, -1] = 1
    # for f in out["frames"]:
    #     f["transform_matrix"] = np.matmul(R, f["transform_matrix"]) # rotate up to be the z axis
    # # find a central point they are all looking at
    # print("computing center of attention...")
    # totw = 0.0
    # totp = np.array([0.0, 0.0, 0.0])
    # for f in out["frames"]:
    #     mf = f["transform_matrix"][0:3,:]
    #     for g in out["frames"]:
    #         mg = g["transform_matrix"][0:3,:]
    #         p, w = closest_point_2_lines(mf[:,3], mf[:,2], mg[:,3], mg[:,2])
    #         if w > 0.00001:
    #             totp += p*w
    #             totw += w
    # if totw > 0.0:
    #     totp /= totw
    # print(totp) # the cameras are looking at totp
    # for f in out["frames"]:
    #     f["transform_matrix"][0:3,3] -= totp
    # avglen = 0.
    # for f in out["frames"]:
    #     avglen += np.linalg.norm(f["transform_matrix"][0:3,3])
    # avglen /= nframes
    # print("avg camera distance from origin", avglen)
    # for f in out["frames"]:
    #     f["transform_matrix"][0:3,3] *= 4.0 / avglen # scale to "nerf sized"
    for f in out["frames"]:
        f["transform_matrix"] = f["transform_matrix"].tolist()
    with open(transforms_file_path, "w") as outfile:
        json.dump(out, outfile, indent=2)
    # with open(images_path+'/pure.json', "w") as outfile:
    #     json.dump(out, outfile, indent=2)
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
def replaceWordInTransformsJson_Not_REMBG(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images', data)
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