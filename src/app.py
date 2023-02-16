from flask import Flask, request,make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from rq import Queue
from rq.job import Job
import redis
import asyncio
import os,time
from dotenv import load_dotenv

from reconstruction import *


load_dotenv()

app=Flask(__name__,static_folder="./data")

# app.config.from_object(os.getenv('APP_SETTINGS'))

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
q = Queue(connection=r)

@app.route('/hello',methods = ['GET'])
def get():
    return 'Hello From Generate3DModel API'

@app.route('/')
def index():
    text = "This is a very long text from your ex"
    # job = q.enqueue(
    #         count_words, text
    #     )
    n = len(q.jobs)

    html = '<center><br /><br />'
    for job in q.jobs:
        html += f'<a href="job/{job.id}">{job.id}</a><br /><br />'
    html += f'Total {n} Jobs in queue </center>'
    return f"{html}"


def createNewModel(user_id,video_path):

    return None

async def update3DModelPath(model_id,model_path):
    pass



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

        job = q.enqueue(
                generate3DModel, args=[reconstruction_configs],result_ttl=86400
            )
        return f'Task {job.get_id()} added to queue at {job.enqueued_at}. {len(q)} tasks in the queue.'

    except Exception as e:
        print(e)
        return make_response(e)





if __name__=="__main__":
    app.run(host='0.0.0.0',port=os.getenv('FLASK_PORT'),debug=True)


