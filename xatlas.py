import pymeshlab
import open3d as o3d


texture_res=4096
texture_dimension=4096
task_name="111_141_obj"
mesh_file_name="111_141_obj"
input_mesh=f"data/{task_name}/{mesh_file_name}.obj"
ext_name=f'_pymeshlab_textdim_{texture_dimension}_texres_{texture_res}'
output=f"data/{task_name}/{mesh_file_name}{ext_name}.obj"


# mesh = o3d.io.read_triangle_mesh(input_mesh)
# mesh.bake_triangle_attr_textures(4096, {task_name})
# mesh.box.bake_vertex_attr_textures(4096, {task_name})


ms = pymeshlab.MeshSet()
ms.load_new_mesh(input_mesh)
ms.compute_texcoord_parametrization_triangle_trivial_per_wedge(textdim=texture_dimension)
# create texture using UV map and vertex colors
ms.compute_texmap_from_color(textname=f"{mesh_file_name}{ext_name}",textw=texture_res,texth=texture_res) # textname will be filename of a png, should not be a full path
# texture file won't be saved until you save the mesh
ms.save_current_mesh(output)
