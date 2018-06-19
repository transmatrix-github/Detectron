# split RealPackage into train and val set
DATA_ROOT=/home/amax/data/securityData
train_list="20180114 20180126 20180403 20180404 20180416 20180417 20180418 20180419 20180420 20180423 20180424 20180425 20180426 20180427 20180428 20180429 20180430 20180502 20180503 20180504 20180508 20180509 20180510 20180511 20180514 20180516 20180517 20180518 20180521 20180522 20180523 20180524 20180528 20180529 20180530 20180601"
test_list="20180507 20180515 20180525 20180531"
mkdir -p $DATA_ROOT/train/Images/Real-Package_train
mkdir -p $DATA_ROOT/train/Images/Real-Package_val
mkdir -p $DATA_ROOT/train/Label/Real-Package_train
mkdir -p $DATA_ROOT/train/Label/Real-Package_val
for f in ${train_list};
  do ln -sn $DATA_ROOT/train/Images/Real-Package/${f} $DATA_ROOT/train/Images/Real-Package_train/${f}; 
done;

for f in ${train_list};
  do ln -sn $DATA_ROOT/train/Label/Real-Package/${f} $DATA_ROOT/train/Label/Real-Package_train/${f}; 
done; 


for f in ${test_list};
  do ln -sn $DATA_ROOT/train/Images/Real-Package/${f} $DATA_ROOT/train/Images/Real-Package_val/${f}; 
done;

for f in ${test_list};
  do ln -sn $DATA_ROOT/train/Label/Real-Package/${f} $DATA_ROOT/train/Label/Real-Package_val/${f};    
done;
