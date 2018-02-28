cd /opt/yushan/caffe
./build/tools/caffe train \
--solver="jobs_actions_org/SSD_512x512_score/solver.prototxt" \
--weights="jobs_actions_org/VGG_SSD_512x512_iter_61000.caffemodel" \
--gpu=0 2>&1 | tee jobs_actions_org/SSD_512x512_score/VGG_VOC0712_SSD_512x512_test.log
