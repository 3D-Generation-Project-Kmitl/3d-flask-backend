
class PipelineDirector:
    def create_reconstruction_pipeline_from_configs(self,builder,reconstruction_configs):
        #draft
        builder.add_image_processing_step(ImageCropResizer())
        builder.add_image_processing_step(ImageDeblurrer())
        builder.add_image_processing_step(ImageRestorer())

        if reconstruction_configs['google_ARCore']=='true':
            builder.add_pose_estimation_step(ARCorePoseEstimator())
        else:
            builder.add_pose_estimation_step(COLMAPPoseEstimator())

        if reconstruction_configs['object_detection']=='true':
            builder.add_background_removal_step(REMBG())
            
        builder.add_3d_reconstruction_step(InstantNeRF())
        builder.add_mesh_processing_step(MeshProcessor())
