import argparse
import os,sys
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

def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		sys.exit(err)

def testGen3DModel():
    args = parse_args()
    if args.m=='full':
        base_folder_path='../../3D_Model_Project/'

        aabb_scale=4
        video_fps_list=[15,30,60]
        colmap_camera_model_list=["PINHOLE","RADIAL","OPENCV"]

        video_path='./data/video/'+args.vi
        for fps in video_fps_list:
            for camera_model in colmap_camera_model_list:
                try:
                    task_name=f'cup_{str(fps)}_{camera_model}'
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


                    do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {video_fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')


                    colmap_images_folder_path='./data/video/images'
                    rembg_images_folder_path=folder_path+'images_png'
                    do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
                    replaceWordInTransformsJson(transforms_file_path)
                    run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
                    output_mesh_file_path=folder_path+f'{task_name}.obj'
                    do_system(f'python {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path}')
                    do_system(f'rm ./data/video/images -r')
                except:
                    print("An exception occurred")
        else:
            base_folder_path='../../3D_Model_Project/'
            aabb_scale=4
            if args.fps=='' or args.camm=='' or args.vi=='':
                print('Please enter video input path or fps or camera model.')
                return 
            video_fps_list=int(args.fps)
            colmap_camera_model_list=args.camm
            video_path='./data/video/'+args.vi

 
            task_name=f'cup_{str(fps)}_{camera_model}'
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


            do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {video_fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')


            colmap_images_folder_path='./data/video/images'
            rembg_images_folder_path=folder_path+'images_png'
            do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
            replaceWordInTransformsJson(transforms_file_path)
            run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
            output_mesh_file_path=folder_path+f'{task_name}.obj'
            do_system(f'python {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path}')
            do_system(f'rm ./data/video/images -r')

    return 'A 3D Model has been generated.'



if __name__=="__main__":
    testGen3DModel()


