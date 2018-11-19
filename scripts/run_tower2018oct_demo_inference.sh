CONFIG=tower2018oct_e2e_faster_rcnn_R-101-FPN_1x.yaml

DETECTRON=/home/amax/workspace/Detectron
OUTPUT_DIR=$DETECTRON/detectron-output/$CONFIG
MODEL=$OUTPUT_DIR/train/tower_train_2018oct/generalized_rcnn/model_iter24999.pkl

DEMO_DIR=/data/liwen/data/towerData/towerData/demo_test_tower2018oct

python2 tools/infer_simple.py \
    --cfg $DETECTRON/configs/exps/$CONFIG \
    --output-dir ./detectron-visualizations \
    --image-ext jpg \
    --wts $MODEL \
    $DEMO_DIR
