DATA_ROOT=/home/amax/data/securityData
LINK_ROOT=/home/amax/workspace/Detectron/lib/datasets/data/security

ln -s $DATA_ROOT/train/Images/Alg-Synthesis $LINK_ROOT/train_Alg-Synthesis
ln -s $DATA_ROOT/train/Images/Auto-Software-Synthesis $LINK_ROOT/train_Auto-Software-Synthesis
ln -s $DATA_ROOT/train/Images/Dongle-Synthesis $LINK_ROOT/train_Dongle-Synthesis
ln -s $DATA_ROOT/train/Images/Pro-Synthesis $LINK_ROOT/train_Pro-Synthesis
ln -s $DATA_ROOT/train/Images/Real-Package $LINK_ROOT/train_Real-Package
ln -s $DATA_ROOT/train/Images/Real-Polyhedron $LINK_ROOT/train_Real-Polyhedron
ln -s $DATA_ROOT/train/Images/Single-Contraband $LINK_ROOT/train_Single-Contraband
ln -s $DATA_ROOT/test/WJP/Dongle-Synthesis/Image $LINK_ROOT/test_Dongle-Synthesis
ln -s $DATA_ROOT/test/WJP/HLX_20180129/Image $LINK_ROOT/test_HLX_20180129
ln -s $DATA_ROOT/test/WJP/MZL_Test_0415/Image $LINK_ROOT/test_MZL_Test_0415
ln -s $DATA_ROOT/test/KongBao/MZL_KongBao_Image $LINK_ROOT/test_MZL_KongBao_Image
ln -s $DATA_ROOT/test/KongBao/Travel-Packages $LINK_ROOT/test_Travel-Packages
ln -s $DATA_ROOT/test/KongBao/ZhongYunZhiHui $LINK_ROOT/test_ZhongYunZhiHui
ln -s $DATA_ROOT/annotations $LINK_ROOT/annotations
