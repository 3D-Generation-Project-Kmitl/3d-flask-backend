from flask import make_response
import aspose.threed as a3d
import time,requests
from helpers import *
from constants import *
from rq import Queue,Retry
import open3d as o3d




def count_words(text):    
    return len(text)

def generate3DModel(reconstruction_configs):

    # waitWhenGPUMemoryLow()
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
    aabb_scale=2
    camera_model="OPENCV"
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
        # change back to /images
        images_path=f'{folder_path}/images'

        unZipImages(raw_data_path,images_path)

        


        if camera_parameter_list is None or not use_google_arcore or camera_parameter_list==[]:
            do_system(f'python3 {colmap2nerf_file_path} --images {images_path} --run_colmap --out {transforms_file_path} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path} --overwrite')
        else:
            saveTransformJson(camera_parameter_list,transforms_file_path,images_path)

        if run_rembg:
            rembg_images_folder_path=folder_path+'images_png'
            do_system(f'rembg p {images_path} {rembg_images_folder_path}')
            replaceWordInTransformsJson(transforms_file_path)
        else:
            replaceWordInTransformsJson_Not_REMBG(transforms_file_path)
            
        run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
        output_mesh_file_path=folder_path+f'{task_name}.obj'
        model_snapshot_path=base_folder_path+'model_snapshot/saved_model.msgpack'

        do_system(f'python3 {run_instant_ngp_file_path} --scene {folder_path} --save_mesh {output_mesh_file_path} --n_steps {n_steps} --save_snapshot {model_snapshot_path} --marching_cubes_res {marching_cubes_res} --save_poisson_mesh {folder_path}')
        
        # mesh=o3d.io.read_triangle_mesh(output_mesh_file_path)
        # no_colored_mesh = o3d.geometry.TriangleMesh()
        # # Get the vertex and face data
        # vertices = mesh.vertices
        # faces = mesh.triangles

        # # Create new face data with vertex indices, texture coordinate indices, and normal indices

            
        # no_colored_mesh.vertices=vertices
        # # Replace the mesh face data with the new data
        # no_colored_mesh.triangles =faces
        # o3d.io.write_triangle_mesh(output_mesh_file_path, no_colored_mesh) 
 
        # print('remove color succeeded')
        scene = a3d.Scene.from_file(output_mesh_file_path)
        file_storage_url=os.getenv('FILE_STORAGE_URL')
        output_mesh_file_path_glb=f'{file_storage_url}/{task_name}/{task_name}.glb'
        scene.save(f'{folder_path}{task_name}.glb')
        sendRequestToUpdate3DModel(model_id,output_mesh_file_path_glb)

        # do_system(f'rm {images_path} -r')
        return output_mesh_file_path_glb
    except Exception as e:
        # do_system(f'rm {images_path} -r')
        print(e)
        return e
def sendRequestToUpdate3DModel(model_id,model_url):
    print('sendRequestToUpdate3DModel',file=sys.stderr)
    model_id=int(model_id)
    print('model_id type',type(model_id))
    r = requests.put(f'{PURECHOO_BACKEND_URL}/model/reconstruction', json ={'modelId':model_id
                                                        ,'model':model_url
                                                        })


# def onSuccess(job, connection, result, *args, **kwargs):
#     print(result)
#     status_code=result[0]
#     reconstruction_configs=result[2]
#     if status_code==0:
#         q = Queue(QUEUE_NAME,connection=connection)
#         q.enqueue(
#                 generate3DModel
#                 ,args=[reconstruction_configs]
#                 ,result_ttl=86400
#                 ,retry=Retry(max=FAILED_JOBS_RETRY)
#             )
