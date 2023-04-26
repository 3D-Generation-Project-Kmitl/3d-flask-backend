import numpy as np
import open3d as o3d
import pyvista as pv
import pymeshlab
import aspose.threed as a3d
import os
# def clean_point_cloud_ultimate(task_path,point_cloud_name):
#     file_path=f'{task_path}/{point_cloud_name}.ply'

#     remove_outlier_file_path=f'{task_path}/{point_cloud_name}_remove_outlier.ply'

#     scaled_file_path=f'{task_path}/{point_cloud_name}_scaled.ply'

#     ply_mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'
#     glb_mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.glb'
#     original_mesh=o3d.io.read_triangle_mesh(file_path)
#     scaled_mesh=original_mesh.scale(0.2,original_mesh.get_center())
#     o3d.io.write_triangle_mesh(scaled_file_path,scaled_mesh)

#     original_point_cloud_o3d=o3d.io.read_point_cloud(file_path)

#     original_point_cloud_o3d_remove_outlier,_=original_point_cloud_o3d.remove_radius_outlier(nb_points=16, radius=0.05)
#     scaled_original_point_cloud_o3d_remove_outlier=original_point_cloud_o3d_remove_outlier.scale(0.50,original_point_cloud_o3d_remove_outlier.get_center())
#     o3d.io.write_point_cloud(remove_outlier_file_path,scaled_original_point_cloud_o3d_remove_outlier)

#     # print("After point cloud:", len(selected_points.points), "points")
#     # o3d.io.write_point_cloud(pcd_output_file_path, selected_points)

#     ms = pymeshlab.MeshSet()
#     ms.load_new_mesh(remove_outlier_file_path)
#     # ms.meshing_decimation_edge_collapse_for_marching_cube_meshes()
#     # ms.compute_normal_for_point_clouds(smoothiter=10,k=100)
#     # ms.apply_normal_point_cloud_smoothing(k=10)
#     ms.generate_surface_reconstruction_screened_poisson(preclean=True,depth=8)
#     ms.apply_coord_two_steps_smoothing(stepsmoothnum=2)
#     # ms.apply_coord_taubin_smoothing(stepsmoothnum=10)
#     ms.save_current_mesh(ply_mesh_output_file_path)
#     scene = a3d.Scene.from_file(ply_mesh_output_file_path)
#     scene.save(glb_mesh_output_file_path)
#     glb_mesh=o3d.io.read_triangle_mesh(ply_mesh_output_file_path)
#     o3d.io.write_triangle_mesh(glb_mesh_output_file_path, glb_mesh)
#     return ply_mesh_output_file_path
def clean_point_cloud(task_path,point_cloud_name):
    file_path=f'{task_path}/{point_cloud_name}.ply'

    scaled_remove_outlier_file_path=f'{task_path}/{point_cloud_name}__scaled_remove_outlier.ply'


    ply_mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'

    original_point_cloud_o3d=o3d.io.read_point_cloud(file_path)

    original_point_cloud_o3d_remove_outlier,_=original_point_cloud_o3d.remove_radius_outlier(nb_points=16, radius=0.05)
    scaled_original_point_cloud_o3d_remove_outlier=original_point_cloud_o3d_remove_outlier.scale(0.2,original_point_cloud_o3d_remove_outlier.get_center())
    o3d.io.write_point_cloud(scaled_remove_outlier_file_path,scaled_original_point_cloud_o3d_remove_outlier)


    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(scaled_remove_outlier_file_path)
    ms.apply_normal_point_cloud_smoothing(k=10)
    ms.generate_surface_reconstruction_screened_poisson(preclean=True,depth=9)
    ms.apply_coord_two_steps_smoothing(stepsmoothnum=2)
    # ms.apply_coord_taubin_smoothing(stepsmoothnum=10)
    ms.save_current_mesh(ply_mesh_output_file_path)


    return ply_mesh_output_file_path


# def clean_point_cloud(task_path,point_cloud_name):
#     file_path=f'{task_path}/{point_cloud_name}.ply'
#     original_mesh=o3d.io.read_triangle_mesh(file_path)
#     scaled_mesh=original_mesh.scale(0.2,original_mesh.get_center())
#     ply_mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'
#     o3d.io.write_triangle_mesh(ply_mesh_output_file_path,scaled_mesh)
#     # scaled_remove_outlier_file_path=f'{task_path}/{point_cloud_name}__scaled_remove_outlier.ply'


#     # ply_mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'

#     # original_point_cloud_o3d=o3d.io.read_point_cloud(file_path)

#     # original_point_cloud_o3d_remove_outlier,_=original_point_cloud_o3d.remove_radius_outlier(nb_points=16, radius=0.05)
#     # scaled_original_point_cloud_o3d_remove_outlier=original_point_cloud_o3d_remove_outlier.scale(0.2,original_point_cloud_o3d_remove_outlier.get_center())
#     # o3d.io.write_point_cloud(scaled_remove_outlier_file_path,scaled_original_point_cloud_o3d_remove_outlier)


#     # ms = pymeshlab.MeshSet()
#     # ms.load_new_mesh(scaled_remove_outlier_file_path)
#     # ms.apply_normal_point_cloud_smoothing(k=10)
#     # ms.generate_surface_reconstruction_screened_poisson(preclean=True,depth=9)
#     # ms.apply_coord_two_steps_smoothing(stepsmoothnum=2)
#     # # ms.apply_coord_taubin_smoothing(stepsmoothnum=10)
#     # ms.save_current_mesh(ply_mesh_output_file_path)

def clean_point_cloud_X(task_path,point_cloud_name,iterations=1):
    file_path=f'{task_path}/{point_cloud_name}.ply'
    # # base_file_path=f'{task_path}/{point_cloud_name}_base.ply'

    # # os.system(f'cp {file_path} {base_file_path}')


    scaled_file_path=f'{task_path}/{point_cloud_name}_scaled.ply'

    # pcd_output_file_path=f'{task_path}/{point_cloud_name}_output.ply'

    # mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'

    # scaled_mesh_output_file_path=f'{task_path}/{point_cloud_name}_scaled_mesh_output.ply'

    # for i in range(iterations):
    #     print("Iteration:",i+1,"/",iterations)
    #     print(f'reading point clouds from {file_path}')
    #     original_point_cloud_o3d=o3d.io.read_point_cloud(file_path)
    #     print("Before point cloud:", len(original_point_cloud_o3d.points), "points")
    #     original_point_cloud_o3d_remove_outlier,_=original_point_cloud_o3d.remove_radius_outlier(nb_points=16, radius=0.05)
    #     remove_outlier_file_path=f'{task_path}/{point_cloud_name}__remove_outlier.ply'
    #     o3d.io.write_point_cloud(remove_outlier_file_path,original_point_cloud_o3d_remove_outlier)
        
    #     scaled_point_cloud_o3d=original_point_cloud_o3d_remove_outlier.scale(0.95,original_point_cloud_o3d_remove_outlier.get_center())
    #     print(f'writing scaled point clouds from {scaled_file_path}')
    #     o3d.io.write_point_cloud(scaled_file_path,scaled_point_cloud_o3d)

    #     print(f'reading point clouds from {remove_outlier_file_path}')
    #     original_point_cloud_pv = pv.read(remove_outlier_file_path)
    #     print(f'reading scaled point clouds from {scaled_file_path}')
    #     scaled_point_cloud_pv=pv.read(scaled_file_path)
    #     surface=scaled_point_cloud_pv.extract_surface()

    #     surface_points = original_point_cloud_pv.select_enclosed_points(surface)
    #     mask = surface_points['SelectedPoints']
    #     enclosed_point_indices = np.where(mask == 0)[0]
    #     selected_points=original_point_cloud_o3d.select_by_index(enclosed_point_indices)



    #     print("After point cloud:", len(selected_points.points), "points")
    #     print(f'writing surface point clouds from {pcd_output_file_path}')
    #     o3d.io.write_point_cloud(pcd_output_file_path, selected_points)


    #     file_path=pcd_output_file_path
    # ms = pymeshlab.MeshSet()
    # print(f'reading surface point clouds from {pcd_output_file_path}')
    # ms.load_new_mesh(pcd_output_file_path)
    # ms.apply_normal_point_cloud_smoothing(k=10)
    # ms.generate_surface_reconstruction_screened_poisson(preclean=True,depth=9)
    # ms.apply_coord_two_steps_smoothing(stepsmoothnum=2)
    # # ms.apply_coord_taubin_smoothing(stepsmoothnum=10)
    # print(f'writing mesh from {mesh_output_file_path}')
    # ms.save_current_mesh(mesh_output_file_path)
    base_mesh=o3d.io.read_point_cloud(file_path)
    scaled_mesh_o3d=base_mesh.scale(1,base_mesh.get_center())
    print(f'writing scaled mesh from {scaled_mesh_o3d}')
    o3d.io.write_point_cloud(scaled_file_path,scaled_mesh_o3d)

filename='6_97'
file_path=f'/volume/data/6_97'
clean_point_cloud_X(file_path,filename,1)


def clean_point_cloud_2(task_path,point_cloud_name):
    file_path=f'{task_path}/{point_cloud_name}.ply'

    remove_outlier_file_path=f'{task_path}/{point_cloud_name}_remove_outlier.ply'

    scaled_file_path=f'{task_path}/{point_cloud_name}_scaled.ply'

    pcd_output_file_path=f'{task_path}/{point_cloud_name}_output.ply'

    mesh_output_file_path=f'{task_path}/{point_cloud_name}_mesh_output.ply'

    original_point_cloud_o3d=o3d.io.read_point_cloud(file_path)
    print("Before point cloud:", len(original_point_cloud_o3d.points), "points")

    original_point_cloud_o3d_remove_outlier=original_point_cloud_o3d.remove_radius_outlier(nb_points=16, radius=0.05)
    o3d.io.write_point_cloud(remove_outlier_file_path,original_point_cloud_o3d_remove_outlier)

    scaled_point_cloud_o3d=original_point_cloud_o3d_remove_outlier.scale(0.95,original_point_cloud_o3d_remove_outlier.get_center())
    scaled_point_cloud_o3d=scaled_point_cloud_o3d.voxel_down_sample(voxel_size=0.05)
    o3d.io.write_point_cloud(scaled_file_path,scaled_point_cloud_o3d)

    original_point_cloud_pv = pv.read(original_point_cloud_o3d_remove_outlier)
    scaled_point_cloud_pv=pv.read(scaled_file_path)
    surface=scaled_point_cloud_pv.extract_surface()

    surface_points = original_point_cloud_pv.select_enclosed_points(surface)
    mask = surface_points['SelectedPoints']
    enclosed_point_indices = np.where(mask == 0)[0]
    selected_points=original_point_cloud_o3d.select_by_index(enclosed_point_indices)



    print("After point cloud:", len(selected_points.points), "points")
    o3d.io.write_point_cloud(pcd_output_file_path, selected_points)

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(pcd_output_file_path)
    # ms.meshing_decimation_edge_collapse_for_marching_cube_meshes()
    # ms.compute_normal_for_point_clouds(smoothiter=10,k=100
    ms.apply_normal_point_cloud_smoothing(k=10)
    ms.generate_surface_reconstruction_screened_poisson(preclean=True,depth=12)
    # ms.apply_coord_two_steps_smoothing(stepsmoothnum=2)
    ms.apply_coord_taubin_smoothing(stepsmoothnum=10)
    ms.save_current_mesh(mesh_output_file_path)
    return mesh_output_file_path


