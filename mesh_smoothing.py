import open3d as o3d
import numpy as np

base_mesh_file_path='/volume/data/4_37'

mesh_file_path=f'{base_mesh_file_path}/4_37.ply'
modified_mesh_file_path=f'{base_mesh_file_path}/4_37_taubin_1.ply'
# Load the mesh
mesh = o3d.io.read_triangle_mesh(mesh_file_path)

print('running smoothing')

# # Compute the normals of the mesh
# mesh.compute_vertex_normals()

# Apply the Bilateral filter with a filter size of 0.02 and a sigma value of 0.05
# mesh = mesh.filter_smooth_taubin(number_of_iterations=50) 

# Step 1: Loop subdivision to increase mesh resolution
# mesh = mesh.subdivide_loop(number_of_iterations=2)

# # Step 2: Laplacian smoothing to further reduce surface noise

# Step 3: Remove non-manifold edges and vertices
# mesh = mesh.remove_non_manifold_edges()
# mesh=mesh.remove_degenerate_triangles()
# mesh=mesh.remove_duplicated_triangles()
# mesh=mesh.remove_duplicated_vertices()
# mesh=mesh.remove_unreferenced_vertices()

# Simplify the mesh by clustering nearby vertices
# mesh=mesh.filter_smooth_simple(number_of_iterations=5)


# target_number_of_triangles=int(np.asarray(mesh.vertices).size*0.1)
# Step 4: Mesh decimation to simplify geometry
# mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=target_number_of_triangles)


# mesh = mesh.remove_non_manifold_edges()
# mesh = mesh.remove_degenerate_triangles()
# mesh = mesh.remove_duplicated_triangles()
# mesh = mesh.remove_duplicated_vertices()
# mesh = mesh.remove_unreferenced_vertices()
mesh = mesh.filter_smooth_taubin(number_of_iterations=1) 
# mesh=mesh.filter_smooth_simple(number_of_iterations=50)
# mesh = mesh.subdivide_midpoint(number_of_iterations=2)
# mesh = mesh.filter_smooth_laplacian(number_of_iterations=1)
# mesh = mesh.filter_smooth_taubin(number_of_iterations=2) 





print('finished smoothing')


o3d.io.write_triangle_mesh(modified_mesh_file_path, mesh)
