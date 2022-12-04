import argparse
import os,sys
import re
import cv2
import datetime
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-vi", default="", help="video input")
    parser.add_argument("-m", default="",choices=['full','manual'], help="test mode")
    parser.add_argument("-fps", default="", help="frame per second")
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

def testGen3DModel():
#     os.environ["CUDA_VISIBLE_DEVICES"] = '1'
    args = parse_args()
    if args.m=='full':
        base_folder_path='../../3D_Model_Project/'
        video_name=['cup15cm_test.mp4','cup30cm_test.mp4','cup60cm_test.mp4']

        for video in video_name:
            video_path='./data/video/'+video
            
            base_fps=getFPSForCOLMAP(video_path)

            
            video_fps_list=[base_fps,2*base_fps]
            aabb_scale=[1,4]
            train_n_steps=[500,30000]

            colmap_camera_model_list=["PINHOLE","RADIAL","OPENCV"]
            for aabb in aabb_scale:
                for n_steps in train_n_steps:
                    for fps in video_fps_list:
                        for camera_model in colmap_camera_model_list:
                            try:
                                video_name=video.split('.')[0]
                                task_name=f'{video_name}_{str(fps)}_{camera_model}_{n_steps}_{aabb}'
                                folder_path=f'./data/{task_name}/'
                                if not os.path.exists(folder_path):
                                    os.mkdir(folder_path)

                                transforms_file_path=folder_path+'transforms.json'
                                video_fps=fps

                                colmap_camera_model=camera_model
                                instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
                                colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'

                                colmap_db_file_path=folder_path+'colmap.db'
                                colmap_text_folder_path=folder_path+'colmap_text'


                                do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {video_fps} --aabb_scale {aabb} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')


                                colmap_images_folder_path='./data/video/images'
                                rembg_images_folder_path=folder_path+'images_png'
                                do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
                                replaceWordInTransformsJson(transforms_file_path)
                                run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
                                output_mesh_file_path=folder_path+f'{task_name}.obj'
                                
                                test_transforms_path='./data/cup_test_4_PINHOLE/transforms.json'
                                
                                do_system(f'python {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path} --n_steps {n_steps} --test_transforms {test_transforms_path} --result_path {folder_path}')
                                do_system(f'rm ./data/video/images -r')
                            except:
                                do_system(f'rm ./data/video/images -r')
                                print("An exception occurred")
    else:
        try:
            base_folder_path='../../3D_Model_Project/'
            
            
            if args.camm=='' or args.vi=='':
                print('Please enter video input path or fps or camera model.')
                return 
            aabb_scale=4
            train_n_steps=500
            
            colmap_camera_model=args.camm
            
            video_path='./data/video/'+args.vi
            video_name=args.vi.split('.')[0]
            base_fps=getFPSForCOLMAP(video_path)
            video_fps=base_fps

            task_name=f'{video_name}_{str(video_fps)}_{colmap_camera_model}'
            folder_path=f'./data/{task_name}/'
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            transforms_file_path=folder_path+'transforms.json'
            
            
          
            instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
            colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
            colmap_db_file_path=folder_path+'colmap.db'
            colmap_text_folder_path=folder_path+'colmap_text'
            do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {video_fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')
            colmap_images_folder_path='./data/video/images'
            rembg_images_folder_path=folder_path+'images_png'
            do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
            replaceWordInTransformsJson(transforms_file_path)
            run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
            output_mesh_file_path=folder_path+f'{task_name}.obj'
            test_transforms_path='./data/cup_test_4_PINHOLE/transforms.json'
            do_system(f'python {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path} --n_steps {train_n_steps} --test_transforms {test_transforms_path} --result_path {folder_path}')
            do_system(f'rm ./data/video/images -r')
        except:
            do_system(f'rm ./data/video/images -r')
            print("An exception occurred")
    return 'A 3D Model has been generated.'



if __name__=="__main__":
    testGen3DModel()


