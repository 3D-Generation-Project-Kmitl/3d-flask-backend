from flask import Flask, request,make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from rq import Queue,Retry
from rq.job import Job
import redis
import asyncio
import os,time

from reconstruction import *
from constants import *



app=Flask(__name__,static_folder="./data")

# app.config.from_object(os.getenv('APP_SETTINGS'))

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=r)

@app.route('/hello',methods = ['GET'])
def get():
    return 'Hello From Generate3DModel API'

@app.route('/')
def index():
    n = len(q.jobs)

    html = '<center><br /><br />'
    for job in q.jobs:
        html += f'<a href="job/{job.id}">{job.id}</a><br /><br />'
    html += f'Total {n} Jobs in queue </center>'
    return f"{html}"

@app.route('/empty')
def emptyQueue():
    q.empty()
    n = len(q.jobs)
    html = '<center><br /><br />'
    for job in q.jobs:
        html += f'<a href="job/{job.id}">{job.id}</a><br /><br />'
    html += f'Queue has been empty.Total {n} Jobs in queue </center>'
    return f"{html}"


@app.route('/gen3DModel',methods = ['POST','GET'])
def addTask():
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
        if request.form['camera_parameter'] is not None:
            reconstruction_configs['camera_data']=json.loads(request.form['camera_parameter'])
        print(f'reconstruction_configs: {reconstruction_configs}',file=sys.stderr)
        
        job = q.enqueue(
                generate3DModel
                , args=[reconstruction_configs]
                ,job_timeout='1h'
                ,retry=Retry(max=FAILED_JOBS_RETRY)
            )
        return f'Task {job.get_id()} added to queue at {job.enqueued_at}. {len(q)} tasks in the queue.'
        return "hello world"
    except Exception as e:
        print(e)
        return make_response(e)


if __name__=="__main__":
    app.run(host='0.0.0.0',port=FLASK_PORT,debug=True)


