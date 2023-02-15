from flask import make_response
import aspose.threed as a3d
import time,requests
from helpers import *
def count_words(text):    
    return len(text)

def generate3DModel(images_zip_path,userId,modelId):

    aabb_scale=4
    camera_model="PINHOLE"
    n_steps=500

    base_folder_path='./'
    images_path=f'{base_folder_path}data/video/images'
    try:
        task_name=f'{userId}_{modelId}_{camera_model}'

        folder_path=f'{base_folder_path}data/{task_name}/'

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        transforms_file_path=folder_path+'transforms.json'
        colmap_camera_model=camera_model
        instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
        colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'

        colmap_db_file_path=folder_path+'colmap.db'
        colmap_text_folder_path=folder_path+'colmap_text'

        unZipImages(images_zip_path,images_path)

        do_system(f'python3 {colmap2nerf_file_path} --images {images_path} --run_colmap --out {transforms_file_path} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')
        colmap_images_folder_path='./data/video/images'
        rembg_images_folder_path=folder_path+'images_png'
        do_system(f'rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
        replaceWordInTransformsJson(transforms_file_path)
        run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
        output_mesh_file_path=folder_path+f'{task_name}.ply'
        model_snapshot_path=base_folder_path+'model_snapshot/saved_model.msgpack'
        do_system(f'python3 {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path} --n_steps {n_steps} --save_snapshot {model_snapshot_path}')
        
        scene = a3d.Scene.from_file(output_mesh_file_path)
        output_mesh_file_path_glb=folder_path+f'{task_name}.glb'
        
        scene.save(output_mesh_file_path_glb)
        do_system(f'rm {images_path} -r')
        try:
            print(output_mesh_file_path_glb)
            return output_mesh_file_path_glb
        except Exception as e:
            print(e)
            return make_response(e)
        
    except Exception as e:
        do_system(f'rm {images_path} -r')
        print(e)
        return make_response(e)