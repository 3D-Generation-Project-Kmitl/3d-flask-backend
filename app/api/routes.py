from flask import Blueprint
from flask import Flask, request,make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from rq import Queue,Retry
from rq.job import Job
import redis
import os
from controllers import ReconstructionController

api_bp=Blueprint("reconstruction_api",__name__)

@api_bp.route('/reconstruction',methods = ['POST'])
def enqueue_reconstruction_task():
    try:

        controller=ReconstructionController()

        controller.enqueue_task(request)
        
        return "Hooray!",200
    
    except Exception as e:
        return make_response(e)