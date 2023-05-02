import pymeshlab
import open3d as o3d
import aspose.threed as a3d
import numpy as np





texture_res_threshold=16384
texture_res=256
texture_dimension=256
task_name="3_78"
mesh_file_name="3_78"
input_mesh=f"data/{task_name}/{mesh_file_name}.ply"
# input_poisson_mesh=f"data/{task_name}/{mesh_file_name}_poisson_scale_0.3.ply"
ext_name=f'_pymeshlab_textdim_{texture_dimension}_texres_{texture_res}_low_tex'
# depth=9
output=f"data/{task_name}/{mesh_file_name}{ext_name}.ply"
output_mesh_file_path_glb=f"data/{task_name}/{mesh_file_name}{ext_name}.glb"

# import pyvista as pv

# # Load point cloud
# cloud = pv.read(input_mesh)


# Load the point cloud data

import numpy as np
from scipy.spatial import Delaunay
import open3d as o3d


# Save the updated point cloud
# o3d.io.write_point_cloud("updated_point_cloud.ply", pcd)

# Select points inside surface mesh
# mask = cloud.select_enclosed_points(scaled_surface,inside_out=True)

# indices = np.where(mask)[0]


# # Extract points outside surface mesh
# cleaned = cloud.extract_points(indices)




# Save cleaned point cloud
# cleaned.save('cleaned.ply')


# pcd=o3d.io.read_point_cloud(input_mesh)
# mesh,densities=o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=depth)
# o3d.io.write_triangle_mesh(input_poisson_mesh, mesh)

ms = pymeshlab.MeshSet()
ms.load_new_mesh(input_mesh)
# scene = a3d.Scene.from_file(input_poisson_mesh)
# scene.save(output_mesh_file_path_glb)
# ms.generate_surface_reconstruction_screened_poisson()
# ms.save_current_mesh(output)

while texture_res<texture_res_threshold:
    try:
        ms.compute_texcoord_parametrization_triangle_trivial_per_wedge(textdim=texture_dimension)

        # # create texture using UV map and vertex colors
        ms.compute_texmap_from_color(textname=f"{mesh_file_name}{ext_name}",textw=texture_res,texth=texture_res) # textname will be filename of a png, should not be a full path
        # texture file won't be saved until you save the mesh
        ms.save_current_mesh(output)
        scene = a3d.Scene.from_file(output)
        scene.save(output_mesh_file_path_glb)
        break
    except:
        texture_dimension*=2


# pcd=o3d.io.read_point_cloud(input_mesh)
# # Scale the point cloud down
# scale = 0.3
# print('center of point cloud ',pcd.get_center())
# scaled_pcd=pcd.scale(scale, center=pcd.get_center())


# # Create a bounding box around the point cloud
# bounding_box = o3d.geometry.AxisAlignedBoundingBox.create_from_points(pcd.points)

# # Filter points outside the bounding box
# pcd_filtered = pcd.crop(bounding_box)
# mesh,densities=o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(scaled_pcd, depth=depth)
# o3d.io.write_triangle_mesh(input_poisson_mesh, mesh)

# scene = a3d.Scene.from_file(input_poisson_mesh)
# scene.save(output_mesh_file_path_glb)