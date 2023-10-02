import redis
from rq import Worker, Queue, Connection
import app


class TaskQueueWorker:
    def __init__(self,connection,queue_name):
        listen = [queue_name]
        with Connection(connection):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
