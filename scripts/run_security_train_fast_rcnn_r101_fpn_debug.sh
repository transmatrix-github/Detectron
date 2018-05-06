CONFIG=security_e2e_faster_rcnn_R-101-FPN_1x.yaml
DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
# DATE=$(date +'%F_%T')
python2 $DETECTRON/tools/train_net.py --skip-test\
    --cfg $DETECTRON/configs/exps/$CONFIG \
    OUTPUT_DIR $OUTPUT_DIR
