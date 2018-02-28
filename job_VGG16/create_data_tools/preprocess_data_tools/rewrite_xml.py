#coding=utf-8
'''
脚本功能：重写xml,但是xml的名字不变，只是修改里面部分内容 （原因是xml有些问题）
错误：<name/>
正确：<name>handsup</name>
'''

import numpy
import os
import xml.dom.minidom
import sys

input_path = "/opt/yushan/caffe/data/actions/benchmark/labels/" #改
output_path = "/opt/yushan/caffe/data/actions/benchmark/labels_1080/"	#改
if not os.path.exists(output_path):
	os.makedirs(output_path)
	
#改name
error = '<name/>'				#改
ok = "<name>handsup</name>"		#改

#改width、height大小
error_width = '</width>'				#改
error_height = '</height>'			#改

ok_width = '<width>1920</width>'				#改
ok_height = '<height>1080</height>'				#改

for dirpath, dirnames, filenames in os.walk(input_path):
	for filename in filenames:	
		if filename.endswith('.xml'):	#获得文件夹下所有的xml
			s = input_path + filename
			print s
			
			fw = open(output_path + filename, "w")	#重写xml
			with open(s, "r") as ann_file:
				lines = ann_file.readlines()
				for l in lines:		#处理xml中有问题的行，其它行重写
					lst = l.strip()  #list
					ll = ''.join(lst)
					
					if ll.endswith(error_width):
						fw.write(ok_width + "\n")
					elif ll.endswith(error_height):
						fw.write(ok_height + "\n") 
					else: 
						fw.write(ll + "\n")
					'''
					if ll == error:
						fw.write(ok + "\n")
					else:
						fw.write(ll + "\n")'''
			fw.close()
				
