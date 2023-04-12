import os
def do_system(arg):
    print(f"==== running: {arg}")
    uid = os.getuid()
    os.setuid(uid)
    err = os.system(arg)
    if err:
        print("FATAL: command failed")
task_name='4_37_render_aabb_scale_offset'
run_instant_ngp_file_path='./instant-ngp/scripts/run.py'
folder_path=f'./data/{task_name}/'
video_camera_path=f'{folder_path}base_cam.json'
video_output=f'{folder_path}{task_name}.mp4'
output_mesh_file_path=f'{folder_path}{task_name}.ply'
n_steps=500
marching_cubes_res=256
do_system(f'python3 {run_instant_ngp_file_path} \
          --scene {folder_path} \
          --save_mesh {output_mesh_file_path} \
          --n_steps {n_steps} \
          --marching_cubes_res {marching_cubes_res} \
          --video_camera_path {video_camera_path} \
          --video_output {video_output} \
          --video_n_seconds 10')