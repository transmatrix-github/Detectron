CONFIG=security3_e2e_faster_rcnn_R-101-FPN_fg0.1_1x.yaml
DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
# DATE=$(date +'%F_%T')
nohup python2 $DETECTRON/tools/train_net.py \
    --cfg $DETECTRON/configs/exps/$CONFIG \
    OUTPUT_DIR $OUTPUT_DIR \
    > $OUTPUT_DIR/train_log.txt &
