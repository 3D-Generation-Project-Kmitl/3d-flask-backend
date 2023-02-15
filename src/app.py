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
    job = q.enqueue(
            count_words, text
        )
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



@app.route('/gen3DModel',methods = ['POST'])
def addTask():

    try:
        f = request.files['images']
        images_zip_path='./data/video/'+secure_filename(f.filename)
        f.save(images_zip_path)

        # removeBackground=request.form['removeBackground']
        # quality=request.form['quality']
        # print('f',f)
        # print('removeBackground',removeBackground)
        # print('quality',quality)
    
        # print('request.json',request.json)

        # newModel=createNewModel(user_id,images_path)
        # print(newModel)
        timestamp=str(time.time())
        text = "This is a very long text from your ex"
        job = q.enqueue(
                count_words, text
            )


        return f'Task {job.get_id()} added to queue at {job.enqueued_at}. {len(q)} tasks in the queue.'

    except Exception as e:
        print(e)
        return make_response(e)





if __name__=="__main__":
    app.run(host='0.0.0.0',port=os.getenv('FLASK_PORT'),debug=True)


