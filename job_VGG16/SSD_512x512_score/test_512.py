import numpy as np
import matplotlib
matplotlib.use('Agg')
import os
import xml.dom.minidom
import cv2
import time
# %matplotlib inline

# Make sure that caffe is on the python path:
caffe_root = '/opt/yushan/caffe'  # this file is expected to be in {caffe_root}/examples
os.chdir(caffe_root)
import sys
sys.path.insert(0, 'python')

import caffe
caffe.set_mode_gpu()
caffe.set_device(0)


from google.protobuf import text_format
from caffe.proto import caffe_pb2

#model_def = '/opt/yushan/caffe/jobs_11_512/deploy_11.prototxt'
#model_weights = '/opt/yushan/caffe/jobs_11_512/VGG_VOC0712_SSD_512x512_iter_220000_p.caffemodel'
#model_weights = '/opt/yushan/caffe/jobs_11_512/VGG_VOC0712_SSD_512x512_iter_105300.caffemodel'
model_def = '/opt/yushan/caffe/jobs_actions_org/SSD_512x512_score/deploy.prototxt'
model_weights = '/opt/yushan/caffe/jobs_actions_org/VGG_SSD_512x512_iter_52000_1.caffemodel'

#model_def = '/opt/yushan/caffe/data/dede/ssd-model/deploy.prototxt'
#model_weights = '/opt/yangmiao/deepdetect/ssd-server/ssd-model/VGG_VOC0712_SSD_512x512_iter_148000.caffemodel'

# load PASCAL VOC labels
labelmap_file = '/opt/yushan/caffe/data/actions/labelmap_voc.prototxt'
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def get_labelname(labelmap, labels):
	num_labels = len(labelmap.item)
	labelnames = []
	if type(labels) is not list:
		labels = [labels]
	for label in labels:
		found = False
		for i in xrange(0, num_labels):
			if label == labelmap.item[i].label:
				found = True
				labelnames.append(labelmap.item[i].display_name)
				break
		assert found == True
	return labelnames

scales=((512,512),)

# function pick = nms(boxes,threshold,type)
def nms(boxes, threshold):
	if boxes.size==0:
		return np.empty((0,3))
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	s = boxes[:,4]
	area = (x2-x1+1) * (y2-y1+1)
	I = np.argsort(s)
	pick = np.zeros_like(s, dtype=np.int16)
	counter = 0
	while I.size>0:
		i = I[-1]
		pick[counter] = i
		counter += 1
		idx = I[0:-1]
		xx1 = np.maximum(x1[i], x1[idx])
		yy1 = np.maximum(y1[i], y1[idx])
		xx2 = np.minimum(x2[i], x2[idx])
		yy2 = np.minimum(y2[i], y2[idx])
		w = np.maximum(0.0, xx2-xx1+1)
		h = np.maximum(0.0, yy2-yy1+1)
		inter = w * h		 
		o = inter / (area[i] + area[idx] - inter)
		I = I[np.where(o<=threshold)]
	pick = pick[0:counter]
	return pick


net = caffe.Net(model_def,		# defines the structure of the model
				model_weights,	# contains the trained weights
				caffe.TEST)		# use test mode (e.g., don't perform dropout)

# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
print(net.blobs['data'].data.shape)
print(model_weights)
save_dir='/opt/yushan/caffe/jobs_actions_org/result_512_52000/'
#orig_image_dir='/opt/yushan/caffe/data/benchmark_crop/pictures'
#orig_image_dir = '/opt/yushan/caffe/data/test'
#orig_image_dir = '/opt/benchmark_bmp'
orig_image_dir='/opt/yushan/caffe/data/actions/pictures/'
orig_image_txt='/opt/yushan/caffe/data/actions/benchmark.txt'
files = []
with open(orig_image_txt, 'rb') as ann_file:
	lines = ann_file.readlines()
	for l in lines:
		lst = l.strip().split()
		if 2==len(lst):
			ll = lst[0]
			files.append( ll[9:] )
from os import path
#files = [x for x in os.listdir(orig_image_dir) if path.isfile(orig_image_dir+os.sep+x)]

num = 0
sum = len(files)
sumtime = 0
for line in files:
	recttotal = []
	imageLabels = []
	start = time.clock()
	#image_path = orig_image_dir + os.sep+line
	image_path = orig_image_dir + line
	#save_detection_path=save_dir+'res_'+line[0:len(line)-4]+'.txt'
	save_detection_path=save_dir+line[0:len(line)-4]+'.txt'
	image=caffe.io.load_image(image_path)
	saveimge = cv2.imread(image_path)
	image_height,image_width,channels=image.shape	
	print(max(image_height,image_width))
	print(image_height,image_width)
	
	detection_result=open(save_detection_path,'wt')
	for scale in scales:
		image_resize_height = scale[0]
		image_resize_width = scale[1]
		transformer = caffe.io.Transformer({'data': (1,3,image_resize_height,image_resize_width)})
		transformer.set_transpose('data', (2, 0, 1))
		transformer.set_mean('data', np.array([104,117,123])) # mean pixel
		transformer.set_raw_scale('data', 255)	# the reference model operates on images in [0,255] range instead of [0,1]
		transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

		net.blobs['data'].reshape(1,3,image_resize_height,image_resize_width)
		transformed_image = transformer.preprocess('data', image)
		net.blobs['data'].data[...] = transformed_image

		# Forward pass.
		detections = net.forward()['detection_out']

		# Parse the outputs.
		det_label = detections[0,0,:,1]
		det_conf = detections[0,0,:,2]
		det_xmin = detections[0,0,:,3]
		det_ymin = detections[0,0,:,4]
		det_xmax = detections[0,0,:,5]
		det_ymax = detections[0,0,:,6]

		print("detections:")
		print detections.shape
		# Get detections with confidence higher than 0.1.
		top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.3]

		top_conf = det_conf[top_indices]
		top_label_indices = det_label[top_indices].tolist()
		top_labels = get_labelname(labelmap, top_label_indices)
		top_xmin = det_xmin[top_indices]
		top_ymin = det_ymin[top_indices]
		top_xmax = det_xmax[top_indices]
		top_ymax = det_ymax[top_indices]
		 

		for i in xrange(top_conf.shape[0]):
			xmin = int(round(top_xmin[i] * image.shape[1]))
			ymin = int(round(top_ymin[i] * image.shape[0]))
			xmax = int(round(top_xmax[i] * image.shape[1]))
			ymax = int(round(top_ymax[i] * image.shape[0]))
			xmin = max(1, xmin)
			ymin = max(1, ymin)
			xmax = min(image.shape[1]-1, xmax)
			ymax = min(image.shape[0]-1, ymax)
			score = top_conf[i]
			label_name = top_labels[i]	
			label_name_index = top_label_indices[i]

			result=str(label_name)+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+' '+str(xmin)+' '+str(ymax)+' '+str(score)+'\n'
			#detection_result.write(result)
			#print(result)	
			
			cv2.rectangle(saveimge,(int(xmin), int(ymin)),(int(xmax),int(ymax)),(0,255,0),2) 
			cv2.putText(saveimge, str(score)[:3], (int(xmin), int(ymin)), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))				   
			cv2.putText(saveimge, str(label_name), (int(xmin)+50, int(ymin)), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255))
		   
			#result1=str(label_name)+' '+str(score)+'\n'
			label_len=len(str(label_name_index))
			result1=str(label_name_index)[:(label_len-2)]+' '+str(score)+'\n'
			detection_result.write(result1)
			
			print(result) 
				   
	end = time.clock()
	print("read: %f s" % (end - start))	 
	sumtime = sumtime + (end - start)
	num = num + 1
	print("complete: %d in %d" % (num,sum))
	detection_result.close() 

	'''xmin = 530
	ymin = 460
	xmax = 1490
	ymax = 960			 
	score ='0.86'
	label_name = 'brickspile'	 

	cv2.rectangle(saveimge,(int(xmin), int(ymin)),(int(xmax),int(ymax)),(0,255,0),2) 
	cv2.putText(saveimge, str(score)[:3], (int(xmin), int(ymin)), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))				   
	cv2.putText(saveimge, str(label_name), (int(xmin)+50, int(ymin)), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255))'''
	
	cv2.imwrite('/opt/yushan/caffe/jobs_actions_org/result_512_52000/'+line,saveimge)	 
print("Time of Picture: %f" % (sumtime/sum))
print('success')



