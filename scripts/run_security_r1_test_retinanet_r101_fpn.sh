CONFIG=security_r1_retinanet_R-101-FPN_1x.yaml
DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
# DATE=$(date +'%F_%T')
nohup python2 $DETECTRON/tools/test_net.py \
    --cfg $DETECTRON/configs/exps/$CONFIG \
    TEST.WEIGHTS ./detectron-output/$CONFIG/train/security_train_real_package_train/retinanet/model_final.pkl \
    OUTPUT_DIR $OUTPUT_DIR > $OUTPUT_DIR/test_log.txt &
