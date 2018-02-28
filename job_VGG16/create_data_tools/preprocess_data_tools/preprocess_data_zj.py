#coding=utf-8
import numpy as np
import os
import random

fw_train = open("train.txt", 'w')
fw_test = open("test.txt", 'w')
ratio = 0.8
folder_path = "/opt/yushan/caffe/data/actions/"

benchmark_lst = []
with open("benchmark.txt", 'rb') as ann_file:
	lines = ann_file.readlines()
	for l in lines:
		lst = l.strip().split()
		if 2==len(lst):
			ll = lst[0]
			benchmark_lst.append( ll[9:len(ll)-4] )
print ("benchmark_lst: ", len(benchmark_lst))
#print ( benchmark_lst )

xml_lst = []
for dirpath, dirnames, filenames in os.walk(folder_path + "labels/"):
	for filename in filenames:
		if filename.endswith('.xml'):
			xml_lst.append( filename[:len(filename)-4] )

num = 0			
for dirpath, dirnames, filenames in os.walk(folder_path + "pictures/"):
	for filename in filenames:
		sample_num = len(filenames) - len(benchmark_lst)
		#print (sample_num, len(filenames), len(benchmark_lst))
		random.shuffle(filenames)
		if filename.endswith('.jpg'):
			l = filename[:len(filename)-4]
			#print ( l )
			if l in  benchmark_lst:
				#print ("11111111111111")
				continue
			else:
				if l in xml_lst:
					if num < int(sample_num*ratio):
						fw_train.write( "pictures/" + filename + " labels/" + l+".xml\n")
					#elif num >= int(sample_num*ratio) and sample_num:
					else:
						fw_test.write( "pictures/" + filename + " labels/" + l+".xml\n")
						#print (num)
					num = num + 1
				
fw_train.close()
fw_test.close()			
