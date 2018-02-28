cd /opt/yushan/caffe
./build/tools/caffe train \
--solver="jobs_actions_anchor46/solver.prototxt" \
--weights="jobs_actions_anchor46/VGG_SSD_512x512_iter_7000.caffemodel" \
--gpu 0 2>&1 | tee jobs_actions_anchor46/VGG_512x512_02_01.log
