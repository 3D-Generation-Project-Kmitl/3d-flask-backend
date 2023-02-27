import os,time
from dotenv import load_dotenv
load_dotenv()

HIGH_MARCHING_CUBES_RES=512 #1024 may cause out of memory
MEDIUM_MARCHING_CUBES_RES=512
LOW_MARCHING_CUBES_RES=256
GPU_MEMORY_THRESHOLD=20000 #MB
QUEUE_NAME='PURECHOO'
FAILED_JOBS_RETRY=1
PURECHOO_BACKEND_URL=os.getenv('PURECHOO_BACKEND_URL')
REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PORT=os.getenv('REDIS_PORT')
FLASK_PORT=os.getenv('FLASK_PORT')
