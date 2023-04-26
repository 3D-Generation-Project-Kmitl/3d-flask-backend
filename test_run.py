import os
import re
# from src.helpers import saveTransformJson,replaceWordInTransformsJson
# from src.constants import *
def replaceWordInTransformsJson(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
        # data = re.sub(r"\"aabb_scale\": .*,", '', data)
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def replaceWordInTransformsJson_Not_REMBG(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images', data)
        # data = re.sub(r"\"aabb_scale\": .*,", '', data)
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def do_system(arg):
    print(f"==== running: {arg}")
    uid = os.getuid()
    os.setuid(uid)
    err = os.system(arg)
    if err:
        print("FATAL: command failed")
def remove_vertex_colors(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith('v '):
            # Split the line by whitespace
            parts = line.split()
            # Remove the RGB values (indices 4 to 6) from the parts list
            parts = parts[:4] + parts[7:]
            # Join the modified parts back into a line
            new_line = ' '.join(parts) + '\n'
            # Append the new line to the list of new lines
            new_lines.append(new_line)
        else:
            # For all other lines, just append them to the list of new lines
            new_lines.append(line)

    # Write the modified lines back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_lines)
def extract_texture(file_path):
    pass
def convert_to_glb(file_path):
    pass


def simplify_mesh(file_path):
    pass
def smooth_mesh(file_path):
    pass
task_name='lego'
run_instant_ngp_file_path='./instant-ngp/scripts/run.py'
folder_path=f'./data/{task_name}/'
# video_camera_path=f'{folder_path}base_cam.json'
# video_output=f'{folder_path}{task_name}.mp4'
output_mesh_file_path=f'{folder_path}{task_name}.ply'
n_steps=500
marching_cubes_res=256
gpuId=0
transforms_file_path=folder_path+'transforms.json'
colmap_camera_model='PINHOLE'
instant_ngp_scripts_folder_path='./instant-ngp/scripts/'
colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
colmap_db_file_path=folder_path+'colmap.db'
colmap_text_folder_path=folder_path+'colmap_text'
images_path=f'{folder_path}images'
aabb_scale=1
# do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
#                       python3 {colmap2nerf_file_path} \
#                       --images {images_path} \
#                       --run_colmap \
#                       --out {transforms_file_path} \
#                       --aabb_scale {aabb_scale} \
#                       --colmap_camera_model {colmap_camera_model} \
#                       --colmap_db {colmap_db_file_path} \
#                       --text {colmap_text_folder_path} \
#                       --overwrite')
# if not os.path.exists(transforms_file_path):
#     colmap_matcher='exhaustive'
#     do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
#               python3 {colmap2nerf_file_path} \
#               --images {images_path} \
#               --run_colmap \
#               --out {transforms_file_path} \
#                 --aabb_scale {aabb_scale} \
#               --colmap_camera_model {colmap_camera_model} \
#               --colmap_db {colmap_db_file_path} \
#               --text {colmap_text_folder_path} \
#               --overwrite \
#               --colmap_matcher {colmap_matcher}')  
# rembg_images_folder_path=folder_path+'images_png'
# rembg_mask_folder_path=folder_path+'masks'
# do_system(f'rembg p -m u2net {images_path} {rembg_images_folder_path}')
# # os.mkdir(rembg_mask_folder_path)
# # do_system(f'rembg p -om -m u2net {images_path} {rembg_mask_folder_path}')
# # for filename in os.listdir(images_path):
# #     if(filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
# #         do_system(f'rembg i -om {images_path}/{filename} {rembg_mask_folder_path}/{filename}')
# replaceWordInTransformsJson(transforms_file_path)


run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
output_mesh_file_path=folder_path+f'{task_name}.ply'
model_snapshot_path='./model_snapshot/saved_model.msgpack'
do_system(f'CUDA_VISIBLE_DEVICES={gpuId} \
                  python3 {run_instant_ngp_file_path} \
                  --scene {folder_path} \
                  --save_mesh {output_mesh_file_path} \
                  --n_steps {n_steps} \
                  --save_snapshot {model_snapshot_path} \
                  --marching_cubes_res {marching_cubes_res}')
                #   --load_snapshot {model_snapshot_path} \

# do_system(f'python3 {run_instant_ngp_file_path} \
#           --scene {folder_path} \
#           --save_mesh {output_mesh_file_path} \
#           --n_steps {n_steps}')



        # #   --marching_cubes_res {marching_cubes_res} \
        # #   --video_camera_path {video_camera_path} \
        # #   --video_output {video_output} \
        #   --video_n_seconds 10)