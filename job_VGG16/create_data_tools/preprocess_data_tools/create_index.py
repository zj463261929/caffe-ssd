#coding=utf-8
import os
import random
from os import path

isOnlyStatisticsName = False 	#True:已知图片文件夹，生成txt；
								#False:已知txt，生成train.txt、test.txt。
if isOnlyStatisticsName: 
	trainval = open("/opt/zhangjing/caffe/caffe/data/actions_new/benchmark/augment/contrastAndBright.txt",'w+')
	#test = open("/opt/zhangjing/caffe/caffe/data/actions_new/benchmark_test1.txt",'w+')
	interval = 10
	orig_image_dir= "/opt/zhangjing/caffe/caffe/data/actions_new/benchmark/augment/contrastAndBright/img/" #"/opt/zhangjing/caffe/data/actions_new/benchmark/pictures_1080_ratio_new_new_ratio_ratio/"
	files = [x for x in os.listdir(orig_image_dir) if path.isfile(orig_image_dir+os.sep+x) and x.endswith('.jpg')]
	random.shuffle(files)
	#print files
	print len(files),len(list(set(files)))  

	lst = []
	for i in xrange(len(files)): 
		file=files[i]
		#print file     
		basename = os.path.splitext(file)[0]
		result = 'benchmark/augment/contrastAndBright/img'+os.sep+file+' '+ 'benchmark/augment/contrastAndBright/xml'+os.sep+basename+'.xml\n'
		lst.append(result)
		trainval.write(result)

	print len(lst),len(list(set(lst)))

else:
	train_num = 0
	test_num = 0
	folder_path = "/opt/zhangjing/caffe/caffe/data/actions_new/"
	trainval = open("/opt/zhangjing/caffe/caffe/data/actions_new/train.txt",'w+')
	test = open("/opt/zhangjing/caffe/caffe/data/actions_new/test.txt",'w+')
	
	with open(folder_path + "all.txt", 'r') as ann_file:
		lines = ann_file.readlines()
		print len(lines),len(list(set(lines)))

		for i in xrange(len(lines)):
			l = lines[i]
			lst = l.strip().split()
			if len(lst)>1:
				if lst[0].endswith('.jpg') and lst[1].endswith('.xml'):
					if os.path.exists(folder_path + lst[0]) and os.path.exists(folder_path + lst[1]):
						if i% 10 < 7:
							trainval.write(l)
							train_num = train_num + 1
						else:
							test.write(l)
							test_num = test_num + 1
					else:
						print ("not exist: ", lst)
	print ("train num: ", train_num)
	print ("test num: ", test_num)
						
	trainval.close()
	test.close()
			







