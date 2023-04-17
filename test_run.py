import os
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
task_name='4_37_aabb_render_aabb'
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