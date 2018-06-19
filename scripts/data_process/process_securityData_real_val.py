# process train and test file lists in RealPakcage
import os
import io
import sys
import json
from PIL import Image
from progressbar import ProgressBar


# hack for utf-8 coding
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

data_root = '/home/amax/data/securityData'

tmp_folder = '/home/amax/data/securityData/tmp_files_realpackage'


# train_sets = ['Real-Package_train',
#              'Real-Package_val']
train_sets = ['Real-Package_val']

datasets = {'train' : train_sets}

def get_data_root(dataset, is_image = True, data_type = 'train'):
    if data_type == 'train':
        if is_image:
            return os.path.join(data_root, 'train/Images', dataset)
        else:
            return os.path.join(data_root, 'train/Label', dataset)
    elif data_type == 'val':
        if is_image:
            return os.path.join(data_root, 'test/WJP', dataset, 'Image')
        else:
            return os.path.join(data_root, 'test/WJP', dataset, 'Label')
    elif data_type == 'test':
        return os.path.join(data_root, 'test/KongBao', dataset)
    else:
        print dataset
        print data_type
        raise
    return None

def get_label_file_names(image_path):
    filename, ext = os.path.splitext(image_path)    
    return [filename + '.txt', filename + '.TXT', image_path + '.txt', image_path + '.TXT']
    
def get_image_file_names(label_path):    
    image_exts = ['.jpg', '.JPG', '.png', '.PNG', '.jpeg', 'JPEG']
    
    filename, ext = os.path.splitext(label_path)
    names = [filename]
    for ext in image_exts:
        names.append(filename+txt)    
    return names

# check if any item in a list exists in the input set, return the first matched or None
def check_list_in_set(input_list, input_set):
    for item in input_list:
        if item in input_set:
            return item
    return None

# read label file, and return bboxs
def parse_label_file(label_path, valid_lables = None):
    bboxs = []
    return None

def get_file_list(root):
    filelist = []
    for path, subdirs, files in os.walk(root, followlinks=True):
        for name in files:
            filepath = os.path.join(path, name)[len(root)+1:]
            filelist.append(filepath)
    return filelist

def check_image_label_pairs(image_list, label_list):    
    # match image file and label files
    valid_pairs = []
    error_image_list = []        
    error_label_list = []
    label_file_set = set(label_list)
    for line in image_list:        
        label_file = check_list_in_set(get_label_file_names(line), label_file_set)
        if label_file is None:
            error_image_list.append(line)
        else:
            valid_pairs.append((line, label_file))
    # get error_label_list
    vimg, vlabel = zip(*valid_pairs)
    error_label_list = list(label_file_set - set(vlabel))
    return valid_pairs, error_image_list, error_label_list

def save_file_list(filelist, filepath):
    with open(filepath, 'wt') as fp:
        for line in filelist:
            fp.write('%s\n' % line)    

def read_image_label_pairs(pair_file):
    lines = file(pair_file).read().split('\n')[:-1]
    res = []
    for line in lines:
        pair = line.split(' ')
        res.append((pair[0], pair[1]))
    return res
    
def save_image_label_pairs(pair_list, pair_file):
    with open(pair_file, 'wt') as fp:
        for pair in pair_list:
            fp.write('%s %s\n' % pair)    

def load_image_list(dataset, data_type):
    print 'Loading image list ... '
    list_file = os.path.join(tmp_folder, 'image_list_%s_%s.txt' % (data_type, dataset))
    if os.path.exists(list_file):
        print 'image list file exists, reading ...'
        return file(list_file).read().split('\n')[:-1]
    else:
        print 'image list file does not exist, generating ...'
        image_root = get_data_root(dataset, is_image=True, data_type = data_type)
        image_list = get_file_list(image_root)
        save_file_list(image_list, list_file)
        print 'Done. Saved image list.'
        return image_list
    
def load_image_label_pairs(dataset, data_type):
    print 'Loading image label pairs ... '
    # check if pair file exists
    pair_file = os.path.join(tmp_folder, 'image_label_pair_%s_%s.txt' % (data_type, dataset))
    if os.path.exists(pair_file):
        print 'pair list file exists, reading ...'
        return read_image_label_pairs(pair_file)
    else:
        print 'pair list file does not exist, generating ...'
        image_list_file = os.path.join(tmp_folder, 'image_list_%s_%s.txt' % (data_type, dataset))
        label_list_file = os.path.join(tmp_folder, 'label_list_%s_%s.txt' % (data_type, dataset))
        
        print 'Loading image list ...'
        if os.path.exists(image_list_file):
            print 'image list file exists, reading ...'
            image_list = file(image_list_file).read().split('\n')[:-1]
        else:
            print 'image list file does not exist, generating ...'
            image_root = get_data_root(dataset, is_image=True, data_type = data_type)
            image_list = get_file_list(image_root)
            save_file_list(image_list, image_list_file)
            print 'Done. Saved image list.'
        
        print 'Loading label list ...'
        if os.path.exists(label_list_file):
            print 'label list file exists, reading ...'
            label_list = file(label_list_file).read().split('\n')[:-1]
        else:
            print 'label list file does not exist, generating ...'
            label_root = get_data_root(dataset, is_image=False, data_type = data_type)
            label_list = get_file_list(label_root)
            save_file_list(label_list, label_list_file)        
            print 'Done. Saved label list.'
        
        print 'Gnerating image label pairs ...'
        valid_pairs, error_image_list, error_label_list = check_image_label_pairs(image_list, label_list)
        save_image_label_pairs(valid_pairs, pair_file)        
        save_file_list(error_image_list, os.path.join(tmp_folder, 'unmatched_image_list_%s_%s.txt' % (data_type, dataset)))
        save_file_list(error_label_list, os.path.join(tmp_folder, 'unmatched_label_list_%s_%s.txt' % (data_type, dataset)))
        print 'Done. In total %d pairs, %d unpaired images, %d unpaired labels ...' % (len(valid_pairs), len(error_image_list), len(error_label_list))
    return valid_pairs

def get_label(key):    
    labels = {'0': 1, 'o':1, 'O':1, 'k': 1, 'K' : 1, # knife
              'y': 2, 'Y':2, # gun,
              'q': 3, 'Q':3, # firecraker
              's': 4, 'S':4, # unknown, need to check with FR
              'x': 5, 'X':5, # unknown, need to check with FR
              'z': 6, 'Z':6, # unknown, need to check with FR
             }
    if key not in labels:
        print key
    assert key in labels
    return labels[key]

def get_categories():
    # define classes
    classes = ['knife', 'gun', 'firecraker', 'S-unknown', 'X-unknown', 'Z-unknown']
    
    categories = []    
    for i, cls in enumerate(classes, 1):
        categories.append({
                'id': i,
                'name': cls,
                'supercategory': 'prohibited_goods'
            })
    return categories

def convert_to_json(pair_list, image_root, label_root, label_set):
    # construct dataset
    dataset = {
        'licenses': [],
        'info': {},
        'categories': get_categories(),
        'images': [],
        'annotations': []
        }    
    if label_root is not None:
        is_pair = True
    else:
        is_pair = False
        
    # append image information, and label information    
    bbox_idx = 0
    img_idx = 0
    error_list = []
    
    pbar = ProgressBar()
    for line in pbar(pair_list): 
        if is_pair:
            image_path = os.path.join(image_root, line[0])        
            label_path = os.path.join(label_root, line[1])
        else:
            image_path = os.path.join(image_root, line)        

	# pickup only default image
	    filename = image_path.split('/')[-1]
	    print filename
	    print image_path
        image_name = '.'.join(filename.split('.')[:-1])
        if not ((image_name[3:6] == 'a01' and image_name[-3] == 'a') or (image_name[3:6] == 'b01' and image_name[-3] == 'd')):
            error_list.append((5, line))
            continue

        # get image information
        try:
            im = Image.open(image_path)
            width, height = im.size
        except Exception:
            print Exception
            # error type 1, image unreadable
            error_list.append((1, line))
            continue
        max_ratio = 4
        if width > height*max_ratio or height > width*max_ratio:
            print 'Abnormal aspect ratio, width = %d, height = %d' %(width, height)
            error_list.append((4, line))
            continue

        if is_pair:
            # get annotation information
            txt_lines = file(label_path).read().split('\n')[:-1]
            valid_count = 0
            for bbox in txt_lines:
                items = bbox.split(' ')
                if len(items) < 5 or len(items[0])!=1:
                    #error type 2, label file format error
                    error_list.append((2, line))
                    break

                if items[0] not in label_set:
                    error_list.append((3, line))
                    break            

                label = get_label(items[0])
                x1 = int(items[1])
                y1 = int(items[2])
                w = int(items[3]) - x1
                h = int(items[4]) - y1

                dataset['annotations'].append({
                        'area': w * h,
                        'bbox': [x1, y1, w, h],
                        'category_id': label,
                        'id': bbox_idx,
                        'image_id': img_idx,
                        'iscrowd': 0,
                        'segmentation': []
                    })

                valid_count += 1
                bbox_idx += 1
                
        # if label file is not valid, this image is removed from training set
        if is_pair and valid_count == 0:
            continue
            
        # end of the image loop, increase img_idx
        dataset['images'].append({
            'coco_url': '',
            'date_captured': '',
            'file_name': image_path,
            'flickr_url': '',
            'id': int(img_idx),
            'license': 0,
            'width': width,
            'height': height
        })
        img_idx += 1
    return dataset, error_list

def save_ignored_list(ignored, ignored_file):
    with open(ignored_file, 'wt') as fp:
        for line in ignored:
            fp.write('%d %s %s\n' %(line[0], line[1][0], line[1][1]))
    
# process training sets
json_folder = os.path.join(data_root, 'annotations')
if not os.path.exists(json_folder):
    os.makedirs(json_folder)

if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)

# label_set = set(['0', 'o', 'O', 'k', 'K', 'y', 'Y', 'q', 'Q'])
label_set = set(['0', 'o', 'O', 'k', 'K', 'y', 'Y'])

for data_type, subsets in datasets.iteritems():
    print '######## Processing %s, in total %d subsets ########' % (data_type, len(subsets))
    for dataset in subsets:
        image_root = get_data_root(dataset, is_image=True, data_type = data_type)
        label_root = get_data_root(dataset, is_image=False, data_type = data_type)
        if data_type == 'test':            
            label_root = None
            valid_pairs = load_image_list(dataset, data_type)            
        else:
            valid_pairs = load_image_label_pairs(dataset, data_type)        
            
        print 'Dataset# %s, #pairs %d' % (dataset, len(valid_pairs))    
        json_data, ignored = convert_to_json(valid_pairs, image_root, label_root, label_set)
        ignored_file = os.path.join(tmp_folder, 'json_ignored_%s_%s.txt' % (data_type, dataset) )            
        save_ignored_list(ignored, ignored_file)
        print '%d pairs are ignored, see %s for detailed information.' % (len(ignored), ignored_file)

        json_file = os.path.join(json_folder, 'instances_%s_%s.json' % (data_type, dataset) )   
        with io.open(json_file, 'wt', encoding='utf8') as fp:
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
            fp.write(unicode(json_str))
        print 'Done'

