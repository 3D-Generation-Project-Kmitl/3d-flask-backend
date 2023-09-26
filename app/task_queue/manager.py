from pipeline.reconstruction import Pipeline

class TaskQueueManager:
    def __init__(self):
        connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.queues = Queue(QUEUE_NAME,connection=connection)
        
    


    def enqueue(self,reconstruction_configs):
        
        reconstruction_pipeline=Pipeline(reconstruction_configs)

        self.queues.enqueue(
                self.reconstruction_pipeline.execute
                , args=[reconstruction_configs]
                ,job_timeout='1h'
            )

    
