#coding=utf-8
'''
脚本功能：统计txt数据集中每个类别的个数、解决样本中类别不均衡的问题。
样本类别均衡化处理：第一步，统计每个类别的个数以及图像只有某个类别的数据信息，使用图像中只有某个类别的图像信息来将其他类别扩充到类别最多的个数；
					第二步，根据7:3的比例划分训练集、验证集；
'''
import  xml.dom.minidom
import numpy as np
import random

bool_only_statistics_classNum = True 	# 改
										#True: 只是统计xml_file中的每个类别的个数
										#False: 对xml_file中的数据做样本类别均衡化处理，并按照7:3生成训练集、验证集。
										
class_name = ["handsup", "like", "hate", "sleep"] #改
class_num = np.zeros(len(class_name))

folder_path = "/opt/zhangjing/caffe/caffe/data/actions_new/" #改
#fw = open(folder_path + "new.txt", 'w') #改
xml_file = open(folder_path + "all.txt", 'r') 	#改
if not bool_only_statistics_classNum:
	fw_train = open(folder_path + "train.txt", 'w') #改
	fw_test = open(folder_path + "test.txt", 'w') #改

handsup_lst = [] #存放xml中只有举手的样本#pictures/0123030269.jpg labels/0123030269.xml，目的是为后面样本类别均衡做准备
like_lst = []
hate_lst = []
sleep_lst = []

lines = xml_file.readlines()
print ("sample num: ", len(lines))
for l in lines:
	ll = l
	lst = l.strip().split()
	if 2==len(lst):	#pictures/0123030269.jpg labels/0123030269.xml
		#打开xml文档
		dom = xml.dom.minidom.parse(folder_path+lst[1]) #用于打开一个xml文件，并将这个文件对象dom变量。
												
		root = dom.documentElement #用于得到dom对象的文档元素，并把获得的对象给root
				
		width_lst = root.getElementsByTagName("width")
		height_lst = root.getElementsByTagName("height")
		width = int(width_lst[0].firstChild.data)	#原始图片宽度
		height = int(height_lst[0].firstChild.data)
					
		xmin_lst = root.getElementsByTagName("xmin")
		ymin_lst = root.getElementsByTagName("ymin")
		xmax_lst = root.getElementsByTagName("xmax")
		ymax_lst = root.getElementsByTagName("ymax")
		'''
		for i in range(len(xmin_lst)):
			print xmin_lst[i].firstChild.data  #获得标签对之间的数据,如：<xmin>418</xmin>'''

		name_lst = []
		lst_temp = root.getElementsByTagName("name")
		for i in range(len(lst_temp)):
			l = lst_temp[i].firstChild.data 
			if l in class_name:
				name_lst.append(l)
		
		#lst1 = list(set(name_lst))#去重后只有一个类别
		if 1==len(name_lst):#len(lst1): 
			if name_lst[0] == "handsup":
				handsup_lst.append(ll)
			if name_lst[0] == "like":
				like_lst.append(ll)
			if name_lst[0] == "hate":
				hate_lst.append(ll)
			if name_lst[0] == "sleep":
				sleep_lst.append(ll)

		num = min(len(name_lst), len(xmin_lst))
		# w/h
		for i in range(num):
			x1 = float(xmin_lst[i].firstChild.data)
			x2 = float(xmax_lst[i].firstChild.data)
			y1 = float(ymin_lst[i].firstChild.data)
			y2 = float(ymax_lst[i].firstChild.data)
			w = x2 - x1 + 0.0
			h = y2 - y1 + 0.0
			if (h>5 and w>5):
				for j in range(len(class_name)):
					if class_name[j] == name_lst[i]:
						class_num[j] = class_num[j] + 1

for j in range(len(class_name)):
	print (class_name[j], class_num[j])

if not bool_only_statistics_classNum:	
	print ("only handsup num: ", len(handsup_lst))
	print ("only like num: ", len(like_lst))
	print ("only hate num: ", len(hate_lst))
	print ("only sleep num: ", len(sleep_lst))
					
	class_num_max = np.max(class_num)
	class_num_maxclass = class_name[np.argmax(class_num)]

	print (class_num_maxclass)

	#handsup
	handsup_lst1 = []
	if len(handsup_lst)>0:
		num = class_num_max - class_num[1]
		d = int(num/len(handsup_lst))
		r = int(num%len(handsup_lst))
		#print (d,r)
		
		for i in range(d):
			like_lst1 = handsup_lst1 + handsup_lst
		handsup_lst1 = handsup_lst1 + handsup_lst[:r]
	#print (len(like_lst1))


	#like
	num = class_num_max - class_num[1]
	d = int(num/len(like_lst))
	r = int(num%len(like_lst))
	#print (d,r)
	like_lst1 = []
	for i in range(d):
		like_lst1 = like_lst1 + like_lst
	like_lst1 = like_lst1 + like_lst[:r]
	#print (len(like_lst1))

	#hate
	num = class_num_max - class_num[2]
	d = int(num/len(hate_lst))
	r = int(num%len(hate_lst))
	#print (d,r)
	hate_lst1 = []
	for i in range(d):
		hate_lst1 = hate_lst1 + hate_lst
	hate_lst1 = hate_lst1 + hate_lst[:r]
	#print (len(hate_lst1))

	#sleep
	num = class_num_max - class_num[3]
	d = int(num/len(sleep_lst))
	r = int(num%len(sleep_lst))
	#print (d,r)
	sleep_lst1 = []
	for i in range(d):
		sleep_lst1 = sleep_lst1 + sleep_lst
	sleep_lst1 = sleep_lst1 + sleep_lst[:r]
	#print (len(sleep_lst1))	

	#样本类别均衡化处理、重写txt
	lines_new = lines + handsup_lst1 + like_lst1 + hate_lst1 + sleep_lst1
	print (len(lines_new))
	'''
	for i in range(len(lines_new)):
		l = lines_new[i]
		fw.write(l)
	fw.close()'''

	#7:3分训练集、验证集
	num_train = 0
	num_test = 0
	random.shuffle(lines_new)
	for i in range(len(lines_new)):
		l = lines_new[i]
		if i%10 < 7:
			fw_train.write(l)
			num_train = num_train + 1
		else:
			fw_test.write(l)
			num_test = num_test + 1
	print ("train.txt: ", num_train)
	print ("test.txt: ", num_test)
	fw_train.close()
	fw_test.close()

