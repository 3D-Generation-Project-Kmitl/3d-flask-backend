from flask import Blueprint
from flask import Flask, request,make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from rq import Queue,Retry
from rq.job import Job
import redis
import os

reconstruction_api=Blueprint("reconstruction_api",__name__)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(QUEUE_NAME,connection=r)

@api.route('/reconstruction',methods = ['POST'])
def enqueue_reconstruction_task():
    try:
        f = request.files['raw_data']
        if not os.path.exists('./data/raw_data/'):
            os.mkdir('./data/raw_data/')
        raw_data_path='./data/raw_data/'+secure_filename(f.filename)
        f.save(raw_data_path)
        reconstruction_configs={}
        reconstruction_configs['raw_data_path']=raw_data_path
        reconstruction_configs['model_id']=request.form['model_id']
        reconstruction_configs['user_id']=request.form['user_id']
        reconstruction_configs['object_detection']=request.form['object_detection']
        reconstruction_configs['quality']=request.form['quality']
        reconstruction_configs['google_ARCore']=request.form['google_ARCore']
        # if request.form['camera_parameter_list'] is not None:
        #     reconstruction_configs['camera_parameter_list']=json.loads(request.form['camera_parameter_list'])
        # else:
        reconstruction_configs['camera_parameter_list']=None
        print(f'reconstruction_configs: {reconstruction_configs}',file=sys.stderr)
        
        job = q.enqueue(
                generate3DModel
                , args=[reconstruction_configs]
                ,job_timeout='1h'
                # ,retry=Retry(max=FAILED_JOBS_RETRY)
            )
        return f'Task {job.get_id()} added to queue at {job.enqueued_at}. {len(q)} tasks in the queue.'
    except Exception as e:
        print(e)
        return make_response(e)