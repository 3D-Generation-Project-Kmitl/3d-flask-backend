import app
from pipeline.builder import PipelineDirector,ReconstructionPipilineBuilder
import redis
from rq import Queue
import TaskQueueWorker

class TaskQueueManager:
    def __init__(self):
        connection = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
        self.queues = Queue(app.config['QUEUE_NAME'],connection=connection)

        self.__start_worker(connection,app.config['QUEUE_NAME'])

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
                ,job_timeout=app.config['QUEUE_JOB_TIMEOUT']
            )
        
    def requeue(self,reconstruction_pipeline):
        self.queues.enqueue(
                reconstruction_pipeline.execute,
                args=[self]
                ,job_timeout=app.config['QUEUE_JOB_TIMEOUT']
            )
    
