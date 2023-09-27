from abc import ABC, abstractmethod


class PipelineBuilderInterface(ABC):
    @abstractmethod
    def add_image_processing_step(self):
        pass
    @abstractmethod
    def add_pose_estimation_step(self):
        pass
    @abstractmethod
    def add_background_removal_step(self):
        pass
    @abstractmethod
    def add_3d_reconstruction_step(self):
        pass
    @abstractmethod
    def add_mesh_processing_step(self):
        pass
    @abstractmethod
    def build(self):
        pass

