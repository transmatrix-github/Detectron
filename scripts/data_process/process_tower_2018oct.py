# process tower data of 2018 oct to be detectron forms
#    + an annotation file
import os
import io
import sys
import json
import codecs
from PIL import Image

# hack for utf-8 coding
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

data_root = '/home/amax/data/towerData/towerData'
image_root = os.path.join(data_root, 'XD_301_30_10_20180906')
json_root = os.path.join(data_root, 'annotations')
if not os.path.exists(json_root):
    os.makedirs(json_root)    

info_file = os.path.join(data_root, 'XD_301_30_10_20180906.txt')

def read_data_info(info_file):    
    data = list()
    info_lines = codecs.open(info_file,  'r', encoding='utf-8').read().split('\n')[:-1]
    info_lines = [line.replace('\r', '') for line in info_lines]    
    for line in info_lines:
        if not line:
            continue
        item  = json.loads(line)    
        data.append(item)
    return data

def get_categories():
    # define classes
    classes = ['XiaoDing']
    
    categories = []    
    for i, cls in enumerate(classes, 1):
        categories.append({
                'id': i,
                'name': cls,
                'supercategory': 'tower'
            })
    return categories

# #########################################################
# read data, and get numbers 
data = read_data_info(info_file)
names = [x['image_name'] for x in data]
names = list(set(names))
print 'In total %d recoders.' % len(data)
print 'In total %d valid images.' % len(names)



###################################################
# construct dataset
dataset = {
    'licenses': [],
    'info': {},
    'categories': get_categories(),
    'images': [],
    'annotations': []
    }    

# append image information
for (image_id, image_name) in enumerate(names):    
    image_path = os.path.join(image_root, image_name)
    # get image information
    try:
        im = Image.open(image_path)
        width, height = im.size
    except Exception:
        print Exception
        continue
        
    dataset['images'].append({
        'coco_url': '',
        'date_captured': '',
        'file_name': image_path,
        'flickr_url': '',
        'id': int(image_id),
        'license': 0,
        'width': width,
        'height': height
    })        
    
# build a map for search image index
name_dict = dict()
for (v, k) in enumerate(names):
    name_dict[k] = v

# append annotation information
bbox_id = 0
for (idx, line) in enumerate(data):    
    image_name = line['image_name']
    image_id = name_dict[image_name]
    print 'Processing [%d/%d] image %s...' %(idx, len(data), image_name)        
    for item in line['data']:
        bbox = item['bbox']
        dataset['annotations'].append({
                'area': bbox['w'] * bbox['h'],
                'bbox': [bbox['x'], bbox['y'], bbox['w'], bbox['h']],
                'category_id': 1,
                'id': bbox_id,
                'image_id': image_id,
                'iscrowd': 0,
                'segmentation': []
            })
        bbox_id += 1

json_file = os.path.join(json_root, 'instances_train_tower2018oct.json')
with io.open(json_file, 'wt', encoding='utf8') as fp:
    json_str = json.dumps(dataset, indent=2, ensure_ascii=False)
    fp.write(unicode(json_str))

print 'Done. In total %d images, %d bboxes' %(len(dataset['images']), len(dataset['annotations']))
