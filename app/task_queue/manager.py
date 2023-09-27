from pipeline.builder import Director,ReconstructionPipilineBuilder

class TaskQueueManager:
    def __init__(self):
        connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.queues = Queue(QUEUE_NAME,connection=connection)
        
    


    def enqueue(self,reconstruction_configs):
        
        director=Director()
        builder=ReconstructionPipilineBuilder()

        director.create_reconstruction_pipeline_from_configs(builder,reconstruction_configs)
        reconstruction_pipeline=builder.build()

        self.queues.enqueue(
                reconstruction_pipeline.execute
                ,job_timeout=1800
            )

    
