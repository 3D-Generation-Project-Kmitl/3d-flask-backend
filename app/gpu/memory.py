import GPUtil
import time
class GPUMemory:
    @staticmethod
    def have_enough_memory(self,required_memory):
        #draft
        waiting_times=0
        while True:
            if waiting_times>2:
                 return False
            # Get all available GPUs
            gpus = GPUtil.getGPUs()
            if len(gpus) > 0:
                # Sort the GPUs by available memory
                gpus = sorted(gpus, key=lambda gpu: gpu.memoryFree, reverse=True)
                # Check available memory of the first GPU
                gpu = gpus[0]
                print(f'{gpu.memoryFree} < {required_memory} ',gpu.memoryFree < required_memory)
                if gpu.memoryFree < required_memory:
                    print(f"Waiting for GPU {gpu.id}... Memory: {gpu.memoryFree} MB")
                    time.sleep(60)  # Wait for 1 minute
                    waiting_times+=1
                else:
                    print(f"GPU {gpu.id} ready! Memory: {gpu.memoryFree} MB")
                    waiting_times=0
                    break  # Exit the loop when the GPU has enough memory
        return True