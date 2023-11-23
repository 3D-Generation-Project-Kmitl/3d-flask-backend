import json
from task_queue.manager import TaskQueueManager
from cloud_storage.manager import CloudStorageManager
class ReconstructionController:
    def __init__(self):

        self.__cloud_storage_manager=CloudStorageManager()
        self.__task_queue_manager=TaskQueueManager()
        self.__image_file=None
        self.__reconstruction_config=dict()

    def __deserialize_request(self,request):
        self.__image_file=request.files['raw_data']
        self.__reconstruction_config=json.load(request.form)

    def __store_image_files(self):
        image_file_name=self.__cloud_storage_manager.store_file(self.__image_file)
        self.__reconstruction_config['image_file_name']=image_file_name

    def enqueue_task(self,request):
        self.__deserialize_request(request)
        self.__store_image_files()
        self.__task_queue_manager.enqueue(self.__reconstruction_config)


    