CONFIG=security3_e2e_faster_rcnn_R-101-FPN_1x.yaml
DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
nohup python2 $DETECTRON/tools/test_net.py \
    --cfg $DETECTRON/configs/exps/$CONFIG \
    TEST.WEIGHTS ./detectron-output/$CONFIG/train/security_train_auto_synthesis\:security_train_pro_synthesis\:security_train_real_package/generalized_rcnn/model_final.pkl \
    OUTPUT_DIR $OUTPUT_DIR/test > $OUTPUT_DIR/test_log.txt &
