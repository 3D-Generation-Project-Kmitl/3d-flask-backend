from flask import Flask, request
from flask_restful import Api,Resource
from werkzeug.utils import secure_filename
import os,sys
import re

app=Flask(__name__)
api=Api(app)

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
class Generate3DModel(Resource):
    def post(self):
        base_folder_path='../../3D_Model_Project/'
        
        aabb_scale=4
        video_fps_list=[15,30,60]
        colmap_camera_model_list=["PINHOLE","RADIAL","OPENCV"]
        
        f = request.files['file']
        video_path='./data/video/'+secure_filename(f.filename)
        f.save(video_path)

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
      
        return 'A 3D Model has been generated.'

    
api.add_resource(Generate3DModel,'/gen3DModel')


if __name__=="__main__":
    app.run(debug=True)


