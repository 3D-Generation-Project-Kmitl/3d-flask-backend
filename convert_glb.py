import os
import aspose.threed as a3d
def do_system(arg):
    print(f"==== running: {arg}")
    uid = os.getuid()
    os.setuid(uid)
    err = os.system(arg)
    if err:
        print("FATAL: command failed")


task_name="111_141_obj"
mesh_file_name="111_141_obj_pymeshlab_textdim_4096_texres_4096"
input_mesh=f"data/{task_name}/{mesh_file_name}.obj"
output=f"data/{task_name}/{mesh_file_name}.glb"

scene = a3d.Scene.from_file(input_mesh)


scene.save(output)