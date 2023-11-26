from flask import Blueprint
from flask import Flask, request,make_response
from ..middleware.auth import auth_required
from .controllers import ReconstructionController

api_bp=Blueprint("reconstruction_api",__name__)

@api_bp.route('/reconstruction',methods = ['POST'])
@auth_required
def enqueue_reconstruction_task():
    try:

        # controller=ReconstructionController()
        # controller.enqueue_task(request)
        
        return "Hooray!",200
    
    except Exception as e:
        return make_response(e)
@api_bp.route('/api',methods = ['GET'])
def hello():
    try:
        
        return "Hello from api"
    
    except Exception as e:
        return make_response(e)
