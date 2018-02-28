#coding=utf-8
import  xml.dom.minidom
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class xml_info(object):
	def __init__(self, input_width, input_height, class_name):
		self.input_width = input_width
		self.input_height = input_height
		self.class_name = class_name

	def get_box_info(self, xml_file, folder_path):
		ratio_lst = []  #存放所有类别box的宽高比
		area_lst = []  	#存放所有类别box的面积
		
		lines = xml_file.readlines()
		for l in lines:
			lst = l.strip().split()
			if 2==len(lst):	#pictures/0123030269.jpg labels/0123030269.xml
				#打开xml文档
				if not os.path.exists( folder_path+lst[1] ):
					continue
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
				'''for i in range(len(xmin_lst)):
					print xmin_lst[i].firstChild.data  #获得标签对之间的数据,如：<xmin>418</xmin>'''

				name_lst = []
				lst_temp = root.getElementsByTagName("name")
				for i in range(len(lst_temp)):
					l = lst_temp[i].firstChild.data 
					if l in self.class_name:
						name_lst.append(l)
						
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
						w = w*self.input_width/width
						h = h*self.input_height/height
						
						area = w*h		
						#print (w,	h, area)
						ratio_lst.append( w/h )
						area_lst.append( area )
					else:
						print ("error xml: ", lst[1],	y2, y1, x1, x2)
					
		return (ratio_lst, area_lst)
	
	#data_lst: 是面积或者宽高比的数值； interval：是采样的间隔；
	#返回值：(interval_lst, num_lst)是采样的数值、采样数据的直方图
	def get_histogram(self, data_lst, interval=20 ):
		lst = []
		for i in range(len(data_lst)):
			#lst.append( int(data_lst[i]*100)/100.0  )
			lst.append( int(data_lst[i]*10000)/10000.0  )
		#print (len(temp))

		interval_lst = []
		for d in np.arange(min(lst), max(lst), interval):
			interval_lst.append( d )
		interval_lst.append( max(lst) )

		num = len(interval_lst) - 1
		num_arr = np.zeros( num )
		for ii in range( len(lst) ):
			data = lst[ii]
			for i in range( num ):
				if num-1 == i:
					if data >=interval_lst[i] and data<=interval_lst[i+1]:
						num_arr[i] = num_arr[i] + 1
				else:
					if data >=interval_lst[i] and data<interval_lst[i+1]:
						num_arr[i] = num_arr[i] + 1
		num_lst = [0]
		for i in range(num):
			num_lst.append( num_arr[i] )
		return (interval_lst, num_lst)		
	
	#将数据分段显示
	def draw_histogram(self, interval_lst, num_lst, level, filename):
		## 'r--'红色的破折号，'bs'蓝色的方块，'g^'绿色的三角形, 'ro' 红色 散点
		color_lst = ['r', 'g', 'b', 'r--', 'g--', 'b--', 'rs', 'gs', 'bs', 'r^', 'g^', 'b^', 'ro', 'go', 'bo']
		if level > len(color_lst):
			level = len(color_lst)
		num = len(interval_lst)
		num1 = num/level
		
		plt.xlim(interval_lst[0], interval_lst[num1])# set axis limits
		plt.ylim(0.0, np.max(num_lst) )
		
		for i in range(level):
			lst_x = []
			lst_y = []
			for ii in range(num1):
				lst_x.append( interval_lst[i*num1 + ii] - interval_lst[i*num1] )
				lst_y.append( num_lst[i*num1 + ii] )
				
			s = "data(" + str(min(lst_x) + interval_lst[i*num1]) + "," + str(max(lst_x) + interval_lst[i*num1]) + ")"
			plt.plot(lst_x, lst_y, color_lst[i], label=s) #


		plt.legend(loc='upper right', shadow=True, fontsize='x-large')# make legend

		plt.title('histogram') 
		plt.xlabel('data')
		plt.ylabel('num')

		plt.show()# show the plot on the screen
		plt.savefig(filename)

	def get_anchor_info(self, ratio_interval, area_interval, area_lst, ratio_lst):
		if ratio_interval[0] > min(ratio_lst):
			ratio_interval.insert(0, int(min(ratio_lst)*100)/100.0 - 1.0)
		num = len(ratio_interval)
		if ratio_interval[num-1] < max(ratio_lst):
			ratio_interval.insert(num, int(max(ratio_lst)*100)/100.0 + 1.0)
		
		#print (area_interval)
		if area_interval[0] > min(area_lst):
			area_interval.insert(0, int(min(area_lst)*100)/100.0 - 1.0)
		num = len(area_interval)
		if area_interval[num-1] < max(area_lst):
			area_interval.insert(num, int(max(area_lst)*100)/100.0 + 1.0)
		#print (area_interval)
		
		level = len(area_interval) - 1
		cols = len(ratio_interval) - 1
		num_arr = np.zeros( (level, cols) )
		for ii in range( len(ratio_lst) ):
			area = int(area_lst[ii]*100)/100.0 
			ratio = int(ratio_lst[ii]*100)/100.0  #保留2位小数点
			
			for row in range(level):
				for col in range(cols):		
					if ( area>=area_interval[row] and area<area_interval[row+1]):
						if (ratio >=ratio_interval[col] and ratio<ratio_interval[col+1]):
							num_arr[row][col] = num_arr[row][col] + 1
			
		return (num_arr, ratio_interval, area_interval)
	
		
#主函数
class_name = ["handsup", "like", "hate", "sleep"] #类别名称, 	改
input_width = 512	#训练网络结构中指定的输入图片宽高，	改
input_height = 512	#	改


folder_path = "/opt/zhangjing/caffe/caffe/data/actions_new/"		#改
xml_file = open(folder_path + "test1.txt", 'r') 	#改

c = xml_info(input_width, input_height, class_name)
ratio_lst, area_lst = c.get_box_info(xml_file, folder_path)	#统计所有xml中类别的宽高比、面积
print ("box num = : ", len(area_lst))

dutyRatio_lst = [] #存放所有类别box的占空比
area = input_width*input_height + 0.0000001
for i in range( len(area_lst) ):
	dutyRatio_lst.append( area_lst[i]/area ) 

#print (dutyRatio_lst)

#以一定间隔为单位来统计面积或宽高比的直方图
interval_lst, num_lst = c.get_histogram(dutyRatio_lst, interval=0.0005) #(ratio_lst, 0.05)
c.draw_histogram(interval_lst, num_lst, 3, "histogram.png") #以图的形式展示出来，interval_lst为x坐标（面积或宽高比的大小），num_lst为y轴（面积或宽高比的个数）


'''
#以一定间隔为单位来统计面积或宽高比的直方图
interval_lst, num_lst = c.get_histogram(area_lst, interval=20) #(ratio_lst, 0.05)
c.draw_histogram(interval_lst, num_lst, 7, "histogram.png") #以图的形式展示出来，interval_lst为x坐标（面积或宽高比的大小），num_lst为y轴（面积或宽高比的个数）

#统计分布
#area_lst = [35.84*35.84, 76.8*76.8, 153.6*153.6, 230.4*230.4, 307.2*307.2, 384.0*384.0, 460.8*460.8, 537.6*537.6] #VGG16 7层
area_interval = [20.48*20.48, 46.72*46.72, 128.57*128.57, 210.42*210.42, 292.27*292.27, 374.12*374.12, 455.97*455.97, 537.6*537.6]# 改
ratio_interval = [0.2,0.25,0.33,0.5,0.7,1.0,1.2,1.4,1.6,2.0]	#改

#统计面积落入某个面积间隔区域内，同时宽高比也落入某个宽高比间隔区域的个数
num_arr, ratio_interval, area_interval = c.get_anchor_info(ratio_interval, area_interval, area_lst, ratio_lst)
print ("area_interval:", area_interval)		
print ("ratio_interval:", ratio_interval)
print ("num: ")					#num_arr的列表示ratio_interval
for row in range(num_arr.shape[0]):	
	print ( num_arr[row][:])
#print ("sum: ", np.sum(num_arr))
'''
xml_file.close()




