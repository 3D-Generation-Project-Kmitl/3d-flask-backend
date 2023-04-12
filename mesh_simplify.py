import open3d as o3d
import numpy as np


pitch=0.05
level=0.5

mesh_name='111_195_marching_256'
ext_name=f'_simplify_pitch_{pitch}_level_{level}'
base_mesh_file_path=f'/volume/data/{mesh_name}'

mesh_file_path=f'{base_mesh_file_path}/{mesh_name}.obj'
pyvista_mesh_output=f'{base_mesh_file_path}/{mesh_name}{ext_name}.ply'
modified_mesh_file_path=f'{base_mesh_file_path}/{mesh_name}{ext_name}.obj'


print('running simplify')
import pyvista as pv

# Load the mesh from a file
mesh = pv.read(mesh_file_path)

# Compute the surface of the mesh
surface_mesh = mesh.extract_surface(nonlinear_subdivision=5)


# Save the surface mesh to a file
surface_mesh.save(pyvista_mesh_output)


# Load the mesh
mesh = o3d.io.read_triangle_mesh(pyvista_mesh_output)



mesh = mesh.remove_non_manifold_edges()
mesh = mesh.remove_degenerate_triangles()
mesh = mesh.remove_duplicated_triangles()
mesh = mesh.remove_duplicated_vertices()
mesh = mesh.remove_unreferenced_vertices()
o3d.io.write_triangle_mesh(modified_mesh_file_path, mesh)

# import trimesh
# import numpy as np
# from skimage import measure

# # Load the mesh from a file
# mesh = trimesh.load(mesh_file_path)

# # Convert the mesh to a voxel grid
# grid = mesh.voxelized(pitch=pitch)

# # Extract the surface mesh using the marching cubes algorithm
# vertices, faces, _, _ = measure.marching_cubes(grid.matrix, level=level)

# # Create a new mesh from the extracted surface
# surface_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

# # Save the surface mesh to a file
# surface_mesh.export(modified_mesh_file_path)