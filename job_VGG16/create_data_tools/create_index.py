import os
import random

from os import path

trainval = open("/opt/yushan/caffe/data/actions/trainval.txt",'w+')
test = open("/opt/yushan/caffe/data/actions/test.txt",'w+')
interval = 10
orig_image_dir="/opt/yushan/caffe/data/actions/pictures"
files = [x for x in os.listdir(orig_image_dir) if path.isfile(orig_image_dir+os.sep+x) and x.endswith('.jpg')]
random.shuffle(files)
#print files

for i in xrange(len(files)): 
    file=files[i]
    print file     
    basename = os.path.splitext(file)[0]
    result = 'pictures'+os.sep+file+' '+ 'labels'+os.sep+basename+'.xml\n'
    if i% 10 == 9:
        test.write(result)
    else:
        trainval.write(result)
        

    
  






