# Python program to explain os.listdir() method 
    
# importing os module 
import os
  
# Get the list of all files and directories
# in the root directory
parent_dir = "/volume/data/"
count=0

import os

# Define the path to the parent directory

# Traverse through all the directories in the parent directory
for dir_name in os.listdir(parent_dir):
    dir_path = os.path.join(parent_dir, dir_name)
    # Check if the directory contains any JPG files
    if not any(filename.endswith('.obj') for filename in os.listdir(dir_path)) and not any(filename.endswith('.ply') for filename in os.listdir(dir_path)) and not any(filename.endswith('.glb') for filename in os.listdir(dir_path)):
        # If not, delete the directory
        # os.system(f'rm -rf {dir_path}')
        print(dir_path)
        count+=1

print(count)