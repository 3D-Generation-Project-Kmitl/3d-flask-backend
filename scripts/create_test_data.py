import argparse
import os,sys
import re
import cv2
import datetime
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-vi", default="", help="video input")
    parser.add_argument("-camm", default="", choices=["SIMPLE_PINHOLE", "PINHOLE", "SIMPLE_RADIAL", "RADIAL","OPENCV"], help="camera model")


    return parser.parse_args()


def replaceWordInTransformsJson(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def getVideoDurationInSeconds(video_path):
    data = cv2.VideoCapture(video_path)
 
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
 
    # calculate duration of the video
    seconds = round(frames / fps)
    return seconds
def getFPSForCOLMAP(video_path):
    fps=128.0/getVideoDurationInSeconds(video_path);
    if fps<1:
        fps=1
    return int(fps)
def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		# sys.exit(err)

def create_test_data():
	os.environ["CUDA_VISIBLE_DEVICES"] = '1'
	args = parse_args()
	base_folder_path='../../3D_Model_Project/'
	video_path='./data/video/'+args.vi
	base_fps=getFPSForCOLMAP(video_path)
	colmap_camera_model=args.camm
	fps=4
	aabb_scale=2
	try:
		video_name=args.vi.split('.')[0]
		task_name=f'{video_name}_{str(fps)}_{colmap_camera_model}'
		folder_path=f'./data/{task_name}/'
		if not os.path.exists(folder_path):
			os.mkdir(folder_path)
			transforms_file_path=folder_path+'transforms.json'
			instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
			colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
			colmap_db_file_path=folder_path+'colmap.db'
			colmap_text_folder_path=folder_path+'colmap_text'
			do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')
			colmap_images_folder_path='./data/video/images'
			rembg_images_folder_path=folder_path+'images_png'
			do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
			replaceWordInTransformsJson(transforms_file_path)
			do_system(f'rm ./data/video/images -r')
	except:
		do_system(f'rm ./data/video/images -r')
		print("An exception occurred")


if __name__=="__main__":
    create_test_data()
