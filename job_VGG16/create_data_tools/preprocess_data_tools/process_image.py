#coding=utf-8
'''
脚本功能：将文件下面的图片大小进行扩充，并保存
作用：将测试图片大小与训练图片大小保持一致。
'''

import os
import numpy as np
import cv2
import random

width = 1920	#改
height = 1080	#改
fw = open("/opt/yushan/caffe/data/actions/benchmark_1080.txt",'w+')	#改
org_image_dir = "/opt/yushan/caffe/data/actions/benchmark/pictures"	#改
save_image_dir = "/opt/yushan/caffe/data/actions/benchmark/pictures_1080" #改
if not os.path.exists(save_image_dir):
	os.makedirs(save_image_dir)

files = [x for x in os.listdir(org_image_dir) if os.path.isfile(org_image_dir+os.sep+x) and x.endswith('.jpg')]
random.shuffle(files)

for i in xrange(len(files)): 
	file=files[i]
	print file	   
	
	#扩充图片大小
	image_path = org_image_dir + "/" + file
	if not os.path.exists(image_path):
		continue
	
	img = cv2.imread(image_path)	
	if img is None:	
		continue

	h = img.shape[0]
	w = img.shape[1]
	if h>height or w>width:
		continue
		
	channels = 3
	if 2==len(img.shape):
		channels = 1
		
	img_new = np.zeros((height,width,channels))
	
	img_new[:h, :w, :channels] = img[:h, :w, :channels]
	cv2.imwrite(save_image_dir + "/" + file, img_new)
	
	#写txt
	basename = os.path.splitext(file)[0]
	result = 'benchmark/pictures_1080'+os.sep+file+' '+ 'benchmark/labels_1080'+os.sep+basename+'.xml\n'
	fw.write(result)
	
fw.close()

