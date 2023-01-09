from flask import Flask, request,make_response,send_from_directory

from werkzeug.utils import secure_filename
import os,sys
import re
import cv2
import datetime
from flask_cors import CORS
import aspose.threed as a3d

app=Flask(__name__,static_folder="./data")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def replaceWordInTransformsJson(transforms_file_path):
    with open(transforms_file_path, 'r') as file:
        data = file.read()
        data = re.sub(r"(?<=\")[^\"]*images", 'images_png', data)
        data =data.replace("jpg", "png")
    with open(transforms_file_path, 'w') as file:
        file.write(data)
def getFPSForCOLMAP(video_path):
    fps=128.0/getVideoDurationInSeconds(video_path);
    if fps<2:
        fps=2
    return int(fps)
def getVideoDurationInSeconds(video_path):
    data = cv2.VideoCapture(video_path)
 
    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)
 
    # calculate duration of the video
    seconds = round(frames / fps)
    return seconds
def do_system(arg):
	print(f"==== running: {arg}")
	err = os.system(arg)
	if err:
		print("FATAL: command failed")
		# sys.exit(err)
@app.route('/hello',methods = ['GET'])
def get():
    return 'Hello From Generate3DModel API'

# @app.route('/data/<folder>/<filename>.obj',methods = ['GET'])
# def get3DModelFile(folder,filename):
#     print(f'/data/{folder}/{filename}.obj')
#     return send_from_directory(f'./data/{folder}', f'{filename}.obj')

@app.route('/gen3DModel',methods = ['POST'])
def post():
    base_folder_path='./'
        
    f = request.files['video']
    video_path='./data/video/'+secure_filename(f.filename)
    envs_path='/home/jupyter-orachat/.conda/envs/dmodel/bin/'
    f.save(video_path)
    fps=getFPSForCOLMAP(video_path)
    aabb_scale=4
    camera_model="PINHOLE"
    n_steps=500

    try:
        video_name=f.filename.split('.')[0]
        task_name=f'{video_name}_{str(fps)}_{camera_model}'
        folder_path=f'data/{task_name}/'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

            transforms_file_path=folder_path+'transforms.json'
            video_fps=fps

            colmap_camera_model=camera_model
            instant_ngp_scripts_folder_path=base_folder_path+'instant-ngp/scripts/'
            colmap2nerf_file_path=instant_ngp_scripts_folder_path+'colmap2nerf.py'
    
            colmap_db_file_path=folder_path+'colmap.db'
            colmap_text_folder_path=folder_path+'colmap_text'


            do_system(f'{envs_path}python3 {colmap2nerf_file_path} --video_in {video_path} --run_colmap --out {transforms_file_path} --video_fps {video_fps} --aabb_scale {aabb_scale} --colmap_camera_model {colmap_camera_model} --colmap_db {colmap_db_file_path} --text {colmap_text_folder_path}')

            colmap_images_folder_path='./data/video/images'
            rembg_images_folder_path=folder_path+'images_png'
            do_system(f'{envs_path}rembg p {colmap_images_folder_path} {rembg_images_folder_path}')
            replaceWordInTransformsJson(transforms_file_path)
            run_instant_ngp_file_path=instant_ngp_scripts_folder_path+'run.py'
            output_mesh_file_path=folder_path+f'{task_name}.ply'
            model_snapshot_path=base_folder_path+'model_snapshot/saved_model.msgpack'
            do_system(f'{envs_path}python3 {run_instant_ngp_file_path} --training_data {folder_path} --mode nerf --save_mesh {output_mesh_file_path} --n_steps {n_steps} --save_snapshot {model_snapshot_path}')
            scene = a3d.Scene.from_file(output_mesh_file_path)
            output_mesh_file_path_glb=folder_path+f'{task_name}.glb'
            scene.save(output_mesh_file_path_glb)
            do_system(f'rm ./data/video/images -r')
            try:
                print(output_mesh_file_path_glb)
                return output_mesh_file_path_glb
            except Exception as e:
                print(e)
                return make_response(e)
        
    except Exception as e:
        do_system(f'rm ./data/video/images -r')
        print(e)
        return make_response(e)
      




if __name__=="__main__":
    app.run(host='0.0.0.0',port=443,debug=True)


