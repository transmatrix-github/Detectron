CONFIG=coco2017_e2e_faster_rcnn_R-101-FPN_1x.yaml
OUTPUT_DIR=./detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
# DATE=$(date +'%F_%T')
nohup python2 tools/train_net.py \
    --cfg configs/exps/$CONFIG \
    OUTPUT_DIR $OUTPUT_DIR \
    > ./detectron-output/$CONFIG/train_log.txt &
