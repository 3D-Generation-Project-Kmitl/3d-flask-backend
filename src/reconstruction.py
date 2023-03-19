from flask import make_response
import aspose.threed as a3d
import time,requests
from helpers import *
from constants import *
from rq import Queue,Retry
import open3d as o3d

import open3d as o3d
import trimesh



def count_words(text):    
    return len(text)

def generate3DModel(reconstruction_configs):

    waitWhenGPUMemoryLow()
    print('hello from generate3DModel', file=sys.stderr)
    print('reconstruction_configs',reconstruction_configs, file=sys.stderr)
    raw_data_path='.'+reconstruction_configs['raw_data_path']
    user_id=str(reconstruction_configs['user_id'])
    model_id=str(reconstruction_configs['model_id'])
    marching_cubes_res=getMarchingCubesRes(reconstruction_configs['quality'])
    if reconstruction_configs['object_detection']=='false':
        run_rembg=False
    else:
        run_rembg=True
    if reconstruction_configs['google_ARCore']=='false':
        use_google_arcore=False
    else:
        use_google_arcore=True

    camera_parameter_list=reconstruction_configs['camera_parameter_list']
    aabb_scale=4
    camera_model="PINHOLE"
    n_steps=1000
    base_folder_path='../'

    try:
        task_name=f'{user_id}_{model_id}'
        folder_path=f'{base_folder_path}data/{task_name}/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        transforms_file_path=folder_path+'transforms.json'
        colmap_camera_model=camera_model
        instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
        colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
        colmap_db_file_path=folder_path+'colmap.db'
        colmap_text_folder_path=folder_path+'colmap_text'

        images_path=f'{folder_path}images'

        unZipImages(raw_data_path,images_path)
        for filepath,dirnames,filenames in os.walk(images_path):
            for filename in filenames:
                do_system(f'python3 {instant_ngp_scripts_folder_path}crop-resize.py -s {IMAGE_WIDTH} {IMAGE_HEIGHT} --outputdir {images_path} {images_path}/{filename}')


        deblurganv2_folder_path=base_folder_path+'DeblurGANv2'
        do_system(f'python3 {deblurganv2_folder_path}/predict.py --weights_path {deblurganv2_folder_path}/pretrained_weights/fpn_inception.h5 --input_folder {images_path} --output_folder {images_path} --configs_path {deblurganv2_folder_path}/config/config.yaml')
        
        
        if camera_parameter_list is None or not use_google_arcore or camera_parameter_list==[]:
            colmap_matcher='sequential'
            do_system(f'python3 {colmap2nerf_file_path} --images {images_path} --run_colmap --out {transforms_file_path} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path} --overwrite --colmap_matcher {colmap_matcher}')
            if not os.path.exists(transforms_file_path):
                colmap_matcher='exhaustive'
                do_system(f'python3 {colmap2nerf_file_path} --images {images_path} --run_colmap --out {transforms_file_path} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path} --overwrite --colmap_matcher {colmap_matcher}')
        else:
            saveTransformJson(camera_parameter_list,transforms_file_path,images_path)
            replaceImageSize(transforms_file_path,IMAGE_WIDTH,IMAGE_HEIGHT)


        if run_rembg:
            rembg_images_folder_path=folder_path+'images_png'
            do_system(f'rembg p {images_path} {rembg_images_folder_path}')
            replaceWordInTransformsJson(transforms_file_path)
        else:
            replaceWordInTransformsJson_Not_REMBG(transforms_file_path)
        
            
        run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
        output_mesh_file_path=folder_path+f'{task_name}.ply'
        model_snapshot_path=base_folder_path+'model_snapshot/saved_model.msgpack'

        do_system(f'python3 {run_instant_ngp_file_path} --scene {folder_path} --save_mesh {output_mesh_file_path} --n_steps {n_steps} --save_snapshot {model_snapshot_path} --marching_cubes_res {marching_cubes_res} --save_poisson_mesh {folder_path}')
        
        scene = a3d.Scene.from_file(output_mesh_file_path)
        file_storage_url=os.getenv('FILE_STORAGE_URL')
        output_mesh_file_path_glb=f'{file_storage_url}/{task_name}/{task_name}.glb'
        scene.save(f'{folder_path}{task_name}.glb')
        sendRequestToUpdate3DModel(model_id,output_mesh_file_path_glb)

        return output_mesh_file_path_glb
    except Exception as e:
        print(e)
        print('sendRequestForFailed3DModel runnning')
        print('model_id ',model_id)
        sendRequestForFailed3DModel(model_id)
        return e
    
def sendRequestToUpdate3DModel(model_id,model_url):
    print('sendRequestToUpdate3DModel',file=sys.stderr)
    model_id=int(model_id)
    print('model_id type',type(model_id))
    r = requests.put(f'{PURECHOO_BACKEND_URL}/model/reconstruction', json ={'modelId':model_id
                                                        ,'model':model_url
                                                        })
    
def sendRequestForFailed3DModel(model_id):
    model_id=int(model_id)
    r = requests.put(f'{PURECHOO_BACKEND_URL}/model/reconstruction', json ={'modelId':model_id
                                                        ,'status':'FAILED'
                                                        })
    print('reponse from 3d backend ',str(r))


