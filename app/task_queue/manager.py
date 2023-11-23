import redis
from rq import Queue
from .worker import TaskQueueWorker
from flask import current_app
import sys,os

from app.pipeline.builder import PipelineDirector,ReconstructionPipilineBuilder

class TaskQueueManager:
    def __init__(self):
        import app
        connection = redis.Redis(host=current_app.config['REDIS_HOST'], port=current_app.config['REDIS_PORT'])
        self.queues = Queue(current_app.config['QUEUE_NAME'],connection=connection)

        self.__start_worker(connection,current_app.config['QUEUE_NAME'])

    def __start_worker(self,connection,queue_name):
        TaskQueueWorker(connection,queue_name)
        
    def enqueue(self,reconstruction_configs):
        
        director=PipelineDirector()
        builder=ReconstructionPipilineBuilder()

        director.create_reconstruction_pipeline_from_configs(builder,reconstruction_configs)
        reconstruction_pipeline=builder.build()

        self.queues.enqueue(
                reconstruction_pipeline.execute,
                args=[self]
                ,job_timeout=current_app.config['QUEUE_JOB_TIMEOUT']
            )
        
    def requeue(self,reconstruction_pipeline):
        self.queues.enqueue(
                reconstruction_pipeline.execute,
                args=[self]
                ,job_timeout=current_app.config['QUEUE_JOB_TIMEOUT']
            )
    
