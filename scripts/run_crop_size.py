import os

def do_system(arg):
    print(f"==== running: {arg}")
    uid = os.getuid()
    os.setuid(uid)
    err = os.system(arg)
    if err:
        print("FATAL: command failed")

images_path='/volume/data/4_37_resized/images_png'

for filepath,dirnames,filenames in os.walk(images_path):
    for filename in filenames:
        do_system(f'CUDA_VISIBLE_DEVICES=1 python3 crop-resize.py -s 600 600 --outputdir {images_path} {images_path}/{filename}')