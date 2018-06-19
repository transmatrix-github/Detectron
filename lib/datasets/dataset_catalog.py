# Copyright (c) 2017-present, Facebook, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

"""Collection of available datasets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


# Path to data dir
_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Required dataset entry keys
IM_DIR = 'image_directory'
ANN_FN = 'annotation_file'

# Optional dataset entry keys
IM_PREFIX = 'image_prefix'
DEVKIT_DIR = 'devkit_directory'
RAW_DIR = 'raw_dir'

# Available datasets
DATASETS = {
    'cityscapes_fine_instanceonly_seg_train': {
        IM_DIR:
            _DATA_DIR + '/cityscapes/images',
        ANN_FN:
            _DATA_DIR + '/cityscapes/annotations/instancesonly_gtFine_train.json',
        RAW_DIR:
            _DATA_DIR + '/cityscapes/raw'
    },
    'cityscapes_fine_instanceonly_seg_val': {
        IM_DIR:
            _DATA_DIR + '/cityscapes/images',
        # use filtered validation as there is an issue converting contours
        ANN_FN:
            _DATA_DIR + '/cityscapes/annotations/instancesonly_filtered_gtFine_val.json',
        RAW_DIR:
            _DATA_DIR + '/cityscapes/raw'
    },
    'cityscapes_fine_instanceonly_seg_test': {
        IM_DIR:
            _DATA_DIR + '/cityscapes/images',
        ANN_FN:
            _DATA_DIR + '/cityscapes/annotations/instancesonly_gtFine_test.json',
        RAW_DIR:
            _DATA_DIR + '/cityscapes/raw'
    },
    'coco_2014_train': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_train2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_train2014.json'
    },
    'coco_2014_val': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_val2014.json'
    },
    'coco_2014_minival': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_minival2014.json'
    },
    'coco_2014_valminusminival': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_valminusminival2014.json'
    },
    'coco_2015_test': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test2015.json'
    },
    'coco_2015_test-dev': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test-dev2015.json'
    },
# coco 2017 datasets, added on 29 April, 2018
# 2017 train = 2014 train + 2014valminusminival
# 2017 val = 2014 minival
    'coco_2017_train': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_train2017',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_train2017.json'
    },
    'coco_2017_val': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2017',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/instances_val2017.json'
    },
    'coco_2017_test': {  # 2017 test uses 2015 test images
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test2017.json',
        IM_PREFIX:
            'COCO_test2015_'
    },
    'coco_2017_test-dev': {  # 2017 test-dev uses 2015 test images
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test-dev2017.json',
        IM_PREFIX:
            'COCO_test2015_'
    },
    'coco_stuff_train': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_train2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/coco_stuff_train.json'
    },
    'coco_stuff_val': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/coco_stuff_val.json'
    },
    'keypoints_coco_2014_train': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_train2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/person_keypoints_train2014.json'
    },
    'keypoints_coco_2014_val': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/person_keypoints_val2014.json'
    },
    'keypoints_coco_2014_minival': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/person_keypoints_minival2014.json'
    },
    'keypoints_coco_2014_valminusminival': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_val2014',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/person_keypoints_valminusminival2014.json'
    },
    'keypoints_coco_2015_test': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test2015.json'
    },
    'keypoints_coco_2015_test-dev': {
        IM_DIR:
            _DATA_DIR + '/coco/coco_test2015',
        ANN_FN:
            _DATA_DIR + '/coco/annotations/image_info_test-dev2015.json'
    },
    'voc_2007_trainval': {
        IM_DIR:
            _DATA_DIR + '/VOC2007/JPEGImages',
        ANN_FN:
            _DATA_DIR + '/VOC2007/annotations/voc_2007_trainval.json',
        DEVKIT_DIR:
            _DATA_DIR + '/VOC2007/VOCdevkit2007'
    },
    'voc_2007_test': {
        IM_DIR:
            _DATA_DIR + '/VOC2007/JPEGImages',
        ANN_FN:
            _DATA_DIR + '/VOC2007/annotations/voc_2007_test.json',
        DEVKIT_DIR:
            _DATA_DIR + '/VOC2007/VOCdevkit2007'
    },
    'voc_2012_trainval': {
        IM_DIR:
            _DATA_DIR + '/VOC2012/JPEGImages',
        ANN_FN:
            _DATA_DIR + '/VOC2012/annotations/voc_2012_trainval.json',
        DEVKIT_DIR:
            _DATA_DIR + '/VOC2012/VOCdevkit2012'
    },
#add security dataset
    'security_20180501_train': {
        IM_DIR:
            _DATA_DIR + '/security/train20180501',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train20180501.json'
    },
    'security_20180501_test': {
        IM_DIR:
            _DATA_DIR + '/security/test20180501',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_test20180501.json'
    },
    'security_train_alg_synthesis': {
        IM_DIR:
            _DATA_DIR + '/security/train_Alg-Synthesis',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Alg-Synthesis.json'
    },
    'security_train_auto_synthesis': {
        IM_DIR:
            _DATA_DIR + '/security/train_Auto-Software-Synthesis',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Auto-Software-Synthesis.json'
    },
    'security_train_dongle_synthesis': {
        IM_DIR:
            _DATA_DIR + '/security/train_Dongle-Synthesis',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Dongle-Synthesis.json'
    },
    'security_train_pro_synthesis': {
        IM_DIR:
            _DATA_DIR + '/security/train_Pro-Synthesis',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Pro-Synthesis.json'
    },
    'security_train_real_package': {
        IM_DIR:
            _DATA_DIR + '/security/train_Real-Package',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Real-Package.json'
    },
    'security_train_real_package_val': {
        IM_DIR:
            _DATA_DIR + '/security/train_Real-Package_val',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Real-Package_val.json'
    },
    'security_train_real_package_train': {
        IM_DIR:
            _DATA_DIR + '/security/train_Real-Package_train',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Real-Package_train.json'
    },
    'security_train_real_package_minus': {
        IM_DIR:
            _DATA_DIR + '/security/train_Real-Package_train',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Real-Package_train_minus.json'
    },
    'security_train_real_polyhedron': {
        IM_DIR:
            _DATA_DIR + '/security/train_Real-Polyhedron',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Real-Polyhedron.json'
    },
    'security_train_single_contraband': {
        IM_DIR:
            _DATA_DIR + '/security/train_Single-Contraband',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_train_Single-Contraband.json'
    },
    'security_val_dongle_synthesis': {
        IM_DIR:
            _DATA_DIR + '/security/test_Dongle-Synthesis',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_val_Dongle-Synthesis.json'
    },
    'security_val_hlx': {
        IM_DIR:
            _DATA_DIR + '/security/test_HLX_20180129',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_val_HLX_20180129.json'
    },
    'security_val_mzl': {
        IM_DIR:
            _DATA_DIR + '/security/test_MZL_Test_0415',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_val_MZL_Test_0415.json'
    },
    'security_test_mzl_kongbao': {
        IM_DIR:
            _DATA_DIR + '/security/test_MZL_KongBao_Image',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_test_MZL_KongBao_Image.json'
    },
    'security_test_travel_packages': {
        IM_DIR:
            _DATA_DIR + '/security/test_Travel-Packages',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_test_Travel-Packages.json'
    },
    'security_test_zhongyunzhihui': {
        IM_DIR:
            _DATA_DIR + '/security/test_ZhongYunZhiHui',
        ANN_FN:
            _DATA_DIR + '/security/annotations/instances_test_ZhongYunZhiHui.json'
    }
}
