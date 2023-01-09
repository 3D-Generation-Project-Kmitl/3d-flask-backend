import os
import cv2
import numpy as np

percentage_list=[]
folder_path='./data/video/images_6/'
for i in range(1,227):
    first = cv2.imread(f'{folder_path}{i:04}.jpg')
    second = cv2.imread(f'{folder_path}{i+1:04}.jpg')

    bitwiseand = cv2.bitwise_and(first, second)

    total = first+second
    total_pixels = total[total>0].shape[0]

    matches = bitwiseand[bitwiseand > 0].shape[0]
    percentage = (100*matches/total_pixels)
    percentage_list.append(percentage)
print('percentage_list: ',percentage_list)
print('average overlap percentage: ',np.mean(percentage_list))
print('std overlap percentage: ',np.std(percentage_list))