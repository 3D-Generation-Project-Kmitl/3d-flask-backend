from flask import Flask, request
from flask_restful import Api,Resource
from werkzeug.utils import secure_filename
import os,sys
import re

app=Flask(__name__)
api=Api(app)

class Generate3DModel(Resource):
    def post(self):
        base_folder_path='../3D_Model_Project/'
        f = request.files['file']
        folder_path='./data/phol/'
        os.mkdir(folder_path)
        video_path=folder_path+secure_filename(f.filename)
        f.save(video_path)
        colmap_out_file_path=folder_path+'transforms.json'

        video_fps=7
        aabb_scale=4
        colmap_camera_model='RADIAL'

        instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'

        colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
      
        do_system(f'python {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {colmap_out_file_path} --video_fps {video_fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model}')
      
      
        colmap_images_folder_path=folder_path+'images'
        rembg_images_folder_path=colmap_images_folder_path+'images_png'
        do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')


        transforms_file_path=colmap_out_file_path+'transform.json'
        replaceWordInTransformsJson(transforms_file_path)

        run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
        do_system(f'python {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh /home/jupyter-orachat/3D_Model_Project/instant-ngp/data/phol/cup/cup_1.obj')
      
        return 'Generating a 3D Model.'

    
api.add_resource(Generate3DModel,'/gen3DModel')


if __name__=="__main__":
    app.run(debug=True)

def replaceWordInTransformsJson(transforms_file_path):
    with open(r'transforms_file_path', 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
    with open(r'transforms_file_path', 'w') as file:
        file.write(data)

def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		sys.exit(err)