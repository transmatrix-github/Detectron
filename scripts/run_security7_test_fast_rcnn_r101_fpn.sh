# CONFIG=security3_e2e_faster_rcnn_R-101-FPN_1x.yaml
# CONFIG=security4_e2e_faster_rcnn_R-101-FPN_1x.yaml
CONFIG=security7_e2e_faster_rcnn_R-101-FPN_1x.yaml
DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
mkdir -p $OUTPUT_DIR
nohup python2 $DETECTRON/tools/test_net.py \
    --cfg $DETECTRON/configs/exps/$CONFIG \
    TEST.WEIGHTS ./detectron-output/$CONFIG/train/security_train_alg_synthesis\:security_train_auto_synthesis:security_train_dongle_synthesis\:security_train_pro_synthesis\:security_train_real_package\:security_train_real_polyhedron\:security_train_single_contraband/generalized_rcnn/model_final.pkl 
    OUTPUT_DIR $OUTPUT_DIR/test > test_log.txt
