#coding=utf-8
'''
脚本功能：将文件下面的图片大小进行扩充，并保存
作用：将测试图片大小与训练图片大小保持一致。
'''

import os
import numpy as np
import cv2
import random

width = 512 #1920 #2880 	#改
height = 512 #1080 #1620 #改  	1620=1080*1.5 (原因是benchmark的占空比范围比训练集的大)
fw = open("/opt/zhangjing/caffe/data/actions/benchmark_16.txt",'w+')	#改  
org_image_dir = "/opt/zhangjing/caffe/data/actions/benchmark_16/pictures"	#改
save_image_dir = "/opt/zhangjing/caffe/data/actions/benchmark_16/pictures_1080" #改
if not os.path.exists(save_image_dir):
	os.makedirs(save_image_dir)

files = [x for x in os.listdir(org_image_dir) if os.path.isfile(org_image_dir+os.sep+x) and x.endswith('.jpg')]
#random.shuffle(files)

for i in xrange(len(files)): 
	file=files[i]
	print file	   
	
	#方法1：扩充图片大小
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
	cv2.imwrite(save_image_dir + "/" + file, img_new)''''''
	
	#方法2：统一缩放到512*512
	'''img_512 = cv2.resize(img,(512,512),interpolation=cv2.INTER_CUBIC)
	cv2.imwrite(save_image_dir + "/" + file, img_512)'''
	
	#写txt
	basename = os.path.splitext(file)[0]
	result = 'benchmark_16/pictures_512'+os.sep+file+' '+ 'benchmark_16/labels_512'+os.sep+basename+'.xml\n'
	fw.write(result)
	
fw.close()

