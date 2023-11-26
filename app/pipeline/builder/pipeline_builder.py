from ...pipeline.reconstruction import ReconstructionPipeline
from .builder_interface import PipelineBuilderInterface

class ReconstructionPipelineBuilder(PipelineBuilderInterface):
    def __init__(self):
        self.image_processor=[]
        self.pose_estimator=[]
        self.background_remover=[]
        self.reconstruction_method=[]
        self.mesh_processor=[]
        
    def add_image_processing_step(self,image_processor):
        self.image_processor.append(image_processor)

    def add_pose_estimation_step(self,pose_estimator):
        self.pose_estimator.append(pose_estimator)

    def add_background_removal_step(self,background_remover):
        self.background_remover.append(background_remover)

    def add_3d_reconstruction_step(self,reconstruction_method):
        self.reconstruction_method.append(reconstruction_method)
 
    def add_mesh_processing_step(self,mesh_processor):
        self.mesh_processor.append(mesh_processor)

    def build(self):
        return ReconstructionPipeline(image_processor=self.image_processor,
                                      pose_estimator=self.pose_estimator,
                                      background_remover=self.background_remover,
                                      reconstruction_method=self.reconstruction_method,
                                      mesh_processor=self.mesh_processor)