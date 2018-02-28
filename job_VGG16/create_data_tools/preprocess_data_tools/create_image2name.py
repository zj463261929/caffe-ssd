#coding=utf-8
'''
脚本功能：已知图片所在文件夹，生成txt；txt内容为pictures/0125040105.jpg labels/0125040105.xml
'''
import numpy as np
import os
import random

fw = open("benchmark_10.txt", 'w')	#改
folder_path = "/opt/yushan/caffe/data/actions/benchmark_netImage_10/"	#改

xml_lst = []
for dirpath, dirnames, filenames in os.walk(folder_path + "labels/"):	#'labels' 可改
	for filename in filenames:
		if filename.endswith('.xml'):
			xml_lst.append( filename[:len(filename)-4] )

num = 0			
for dirpath, dirnames, filenames in os.walk(folder_path + "pictures/"):	#"pictures/" 可改
	for filename in filenames:
		#random.shuffle(filenames)
		if filename.endswith('.jpg') or filename.endswith('.bmp') or filename.endswith('.png'):
			l = filename[:len(filename)-4]
			if l in xml_lst:
				fw.write( "pictures/" + filename + " labels/" + l+".xml\n")
				num = num + 1
				
print ("sample num: ", num)
			


