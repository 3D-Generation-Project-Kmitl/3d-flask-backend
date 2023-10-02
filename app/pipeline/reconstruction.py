from gpu import GPUMemory
class ReconstructionPipiline:
    def __init__(self,image_processor,pose_estimator,background_remover,reconstruction_method,mesh_processor):
        self.image_processor=image_processor
        self.pose_estimator=pose_estimator
        self.background_remover=background_remover
        self.reconstruction_method=reconstruction_method
        self.mesh_processor=mesh_processor


    def execute(self,task_queue_manager):
        if GPUMemory.have_enough_memory():
            [ip.execute() for ip in self.image_processor]
            [pe.execute() for pe in self.pose_estimator]
            [br.execute() for br in self.background_remover]
            [rm.execute() for rm in self.reconstruction_method]
            [mp.execute() for mp in self.mesh_processor]
        else:
            task_queue_manager.requeue(self)


        
    