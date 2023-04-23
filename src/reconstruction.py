from flask import make_response
import aspose.threed as a3d
import time,requests
from helpers import *
from constants import *
from rq import Queue,Retry
import open3d as o3d
import redis
import open3d as o3d
import trimesh
import pymeshlab



r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(QUEUE_NAME,connection=r)

def generate3DModel(reconstruction_configs):

    
    print('hello from generate3DModel', file=sys.stderr)
    print('reconstruction_configs',reconstruction_configs, file=sys.stderr)
    raw_data_path='.'+reconstruction_configs['raw_data_path']
    user_id=str(reconstruction_configs['user_id'])
    model_id=str(reconstruction_configs['model_id'])
    marching_cubes_res=getMarchingCubesRes(reconstruction_configs['quality'])


    if reconstruction_configs['object_detection']=='false':
        run_rembg=False
        aabb_scale=16
    else:
        run_rembg=True
        aabb_scale=1

    if reconstruction_configs['google_ARCore']=='false':
        use_google_arcore=False
    else:
        use_google_arcore=True

    camera_parameter_list=reconstruction_configs['camera_parameter_list']
    camera_model="PINHOLE"
    n_steps=500
    base_folder_path='../'

    shouldRequeue,gpuId=waitWhenGPUMemoryLow(marching_cubes_res)
    if shouldRequeue:
        job = q.enqueue(
        generate3DModel
        , args=[reconstruction_configs]
        ,job_timeout='1h'
        # ,retry=Retry(max=FAILED_JOBS_RETRY)
        )
        return "Requeued this job"
    gpuId=str(gpuId)
    os.environ["CUDA_VISIBLE_DEVICES"]=gpuId
    do_system(f'export CUDA_VISIBLE_DEVICES={gpuId}')
    print('gpuId: ',gpuId)
    try:
        task_name=f'{user_id}_{model_id}'
        folder_path=f'{base_folder_path}data/{task_name}/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        else:
            do_system(f'rm -r {folder_path}')
            os.mkdir(folder_path)
        transforms_file_path=folder_path+'transforms.json'
        colmap_camera_model=camera_model
        instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
        colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
        colmap_db_file_path=folder_path+'colmap.db'
        colmap_text_folder_path=folder_path+'colmap_text'
        images_path=f'{folder_path}images'
        unZipImages(raw_data_path,images_path)

        if haveOnlyOneImageResolution(images_path):
            image_width=720
            image_height=1280
        else:
            image_width=IMAGE_WIDTH
            image_height=IMAGE_HEIGHT
        for filename in os.listdir(images_path):
            if(filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
                do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                          python3 {instant_ngp_scripts_folder_path}crop-resize.py \
                          -s {image_width} {image_height} \
                          --outputdir {images_path} {images_path}/{filename}')

        deblurganv2_folder_path=base_folder_path+'DeblurGANv2'
        do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                  python3 {deblurganv2_folder_path}/predict.py \
                  --weights_path {deblurganv2_folder_path}/pretrained_weights/fpn_inception.h5 \
                  --input_folder {images_path} \
                  --output_folder {images_path} \
                  --configs_path {deblurganv2_folder_path}/config/config.yaml')
        r=sendRequestToRestoreImage(images_path)
        print(r)


        if camera_parameter_list is None or not use_google_arcore or camera_parameter_list==[]:
            colmap_matcher='sequential'
            do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                      python3 {colmap2nerf_file_path} \
                      --images {images_path} \
                      --run_colmap \
                      --out {transforms_file_path} \
                      --aabb_scale {aabb_scale} \
                      --colmap_camera_model {colmap_camera_model} \
                      --colmap_db {colmap_db_file_path} \
                      --text {colmap_text_folder_path} \
                      --overwrite \
                      --colmap_matcher {colmap_matcher}')
            if not os.path.exists(transforms_file_path):
                colmap_matcher='exhaustive'
                do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                          python3 {colmap2nerf_file_path} \
                          --images {images_path} \
                          --run_colmap \
                          --out {transforms_file_path} \
                            --aabb_scale {aabb_scale} \
                          --colmap_camera_model {colmap_camera_model} \
                          --colmap_db {colmap_db_file_path} \
                          --text {colmap_text_folder_path} \
                          --overwrite \
                          --colmap_matcher {colmap_matcher}')
        else:
            saveTransformJson(camera_parameter_list,transforms_file_path,images_path)
            replaceImageSize(transforms_file_path,IMAGE_WIDTH,IMAGE_HEIGHT)
        if run_rembg:
            rembg_images_folder_path=folder_path+'images_png'
            rembg_mask_folder_path=folder_path+'masks'
            do_system(f'rembg p -m u2net {images_path} {rembg_images_folder_path}')
            os.mkdir(rembg_mask_folder_path)
            do_system(f'rembg p -om -m u2net {images_path} {rembg_mask_folder_path}')
            # for filename in os.listdir(images_path):
            #     if(filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
            #         do_system(f'rembg i -om {images_path}/{filename} {rembg_mask_folder_path}/{filename}')
            replaceWordInTransformsJson(transforms_file_path)
        else:
            replaceWordInTransformsJson_Not_REMBG(transforms_file_path)


        run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
        output_mesh_file_path=folder_path+f'{task_name}.ply'
        model_snapshot_path=base_folder_path+'model_snapshot/saved_model.msgpack'
        do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                  python3 {run_instant_ngp_file_path} \
                  --scene {folder_path} \
                  --save_mesh {output_mesh_file_path} \
                  --n_steps {n_steps} \
                  --save_snapshot {model_snapshot_path} \
                  --marching_cubes_res {marching_cubes_res}')
                #   --load_snapshot {model_snapshot_path} \

        mesh_name=None
        if reconstruction_configs['quality']=='High':
            mesh_name=f'{task_name}_High'
            cleaned_mesh_path=clean_point_cloud(folder_path,task_name)
            o3d.io.write_triangle_mesh(f'{folder_path}{mesh_name}.glb', cleaned_mesh_path)
        else:

            texture_res_threshold=65536
            texture_res=4096
            texture_dimension=4096
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(output_mesh_file_path)

            while texture_res<texture_res_threshold:
                try:
                    mesh_name=f'{task_name}_pymeshlab_{texture_res}'
                    mesh_ply_path=folder_path+f'{mesh_name}.ply'
                    mesh_glb_path=folder_path+f'{mesh_name}.glb'
                    ms.compute_texcoord_parametrization_triangle_trivial_per_wedge(textdim=texture_dimension)

                    # # create texture using UV map and vertex colors
                    ms.compute_texmap_from_color(textname=f'{task_name}_pymeshlab',textw=texture_res,texth=texture_res) # textname will be filename of a png, should not be a full path
                    # texture file won't be saved until you save the mesh
                    ms.save_current_mesh(mesh_ply_path)

                    original_mesh=o3d.io.read_triangle_mesh(mesh_ply_path)
                    scaled_mesh=original_mesh.scale(0.2,original_mesh.get_center())
                    o3d.io.write_triangle_mesh(mesh_ply_path,scaled_mesh)
                    o3d.io.write_triangle_mesh(mesh_glb_path,scaled_mesh)
                    break
                except Exception as e:
                    print('error message ',e)
                    print('texture_res ',texture_res)
                    print('texture_dimension ',texture_dimension)
                    texture_res*=2
                    texture_dimension*=2


        file_storage_url=os.getenv('FILE_STORAGE_URL')
        output_mesh_file_path_glb=f'{file_storage_url}/{task_name}/{mesh_name}.glb'
        sendRequestToUpdate3DModel(model_id,output_mesh_file_path_glb)

        return output_mesh_file_path_glb
    except Exception as e:
        print(e)
        print('sendRequestForFailed3DModel runnning')
        print('model_id ',model_id)
        # sendRequestForFailed3DModel(model_id)
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

def sendRequestToRestoreImage(images_path):
    print('sendRequestToRestoreImage',file=sys.stderr)
    r = requests.post(f'http://devcontainer-real-esrgan-1:5000/imageRestoration', json ={'images_path':images_path
                                                        })
    return r


