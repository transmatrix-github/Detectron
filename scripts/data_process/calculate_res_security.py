import json
import os
import sys

MAX_IMAGE_NUM = 100000
#check detection errors
def calc_iou(r1, r2):
    ox1 = max(r1[0], r2[0])
    oy1 = max(r1[1], r2[1])
    ox2 = min(r1[0]+r1[2], r2[0]+r2[2])
    oy2 = min(r1[1]+r1[3], r2[1]+r2[3])
    oa = (ox2 - ox1)*(oy2 - oy1)
    return oa*1.0/(r1[2]*r1[3]+r2[2]*r2[3] - oa)

def load_json_file(json_file):
    with open(json_file, 'rt') as fp:
        return json.load(fp)

def group_bboxs(obj_list):    
    im_num = 0
    im_bboxs = [list() for i in range(MAX_IMAGE_NUM)]
    for obj in obj_list:
        im_bboxs[obj['image_id']].append(obj)
        im_num = max(im_num, obj['image_id'])
    return im_bboxs[:im_num + 1]

# return a list, number of images, each det is correct or not, with score
def judge_detection_results(dets, gt=None, iou=0.5):
    is_kongbao = (gt is None)
    
    res = []    
    for im_idx, im_det in enumerate(dets):
        if is_kongbao:            
            max_score = 0
            for obj in im_det:
                max_score = max(max_score, obj['score'])
            judge = (0, max_score)            
        else:
            # normal image, find the max_score for corrected ones.            
            max_score = 0
            for obj1 in im_det:
                max_score = max(max_score, obj1['score'])                        
#             for obj1 in im_det:
#                 for obj2 in gt[im_idx]:
#                     if calc_iou(obj1['bbox'], obj2['bbox']) >= iou:
#                         max_score = max(max_score, obj1['score'])                        
            judge = (1, max_score)
            
        res.append(judge)    
    return res

def generate_roc(wjp, kb):
    # the first version
    # 1. A WJP image is correct, if and only if one of its det is correct
    # 2. A KongBao image is correct, if and only if none of its det is correct
    # 
    # We calculate roc as follows:
    # 1) keep only the max score det for each image, so once thres is setup, best results of KongBao and WJP is obtained.
    # 2) sort WJP and KongBao together, WJP is 1, KongBao is 0
    # 3) detection rate is given by how much percentage of WJP images are detected, 
    #    and false detection rate is given by how much percentage of KongBao images are detected,
    #    judged by aboving a given threshold, which will decrease by iterating the sorted scores from 1 to 0.
    wjp_num = len(wjp)
    kb_num = len(kb)
    print 'In total %d WJP, and %d KB' %(wjp_num, kb_num)
    dets = wjp + kb
    dets.sort(key=lambda x: -x[1])
    wjp_hits = 0
    kb_hits = 0
    roc = []
    for x in dets:
        if x[0] == 0:
            kb_hits += 1
        else:
            wjp_hits += 1
        roc.append((wjp_hits*1.0/wjp_num, kb_hits*1.0/kb_num, x[1]))
    return roc

def get_threshold_by_false_rate(roc, fr):
    for (idx, item) in enumerate(roc):
        if item[1] > fr:
            return roc[idx-1]
    return roc[-1]

def get_res_folder(model):
    if len(model) < 8:
        model = 'security' + model[1:]
        
    if model == 'security7' or model == 'security4' or model == 'security3':
        return model + '_e2e_faster_rcnn_R-101-FPN_1x.yaml'
    elif model == 'security4_ms' or model == 'security3_ms':
        return model[:8] + '_e2e_faster_rcnn_R-101-FPN_ms_1x.yaml'
    else:
        print 'None-Supported model %s' % model
        raise
    return None
    
# plot_roc
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:"
        print '\tpython %s model' % (__file__)
        print '\t-- model: security7 security4 security4_ms security3 or security3_ms'
        sys.exit(0)

output_root = '/home/amax/workspace/Detectron/detectron-output'
val_data = 'security_val_mzl'
test_data = 'security_test_mzl_kongbao'
model_name =  get_res_folder(sys.argv[1])
gt_data = load_json_file('/home/amax/data/securityData/annotations/instances_val_MZL_Test_0415.json')
val_res_file = os.path.join(output_root, model_name, 'test/test/%s/generalized_rcnn/bbox_%s_results.json' % (val_data, val_data))
test_res_file = os.path.join(output_root, model_name, 'test/test/%s/generalized_rcnn/bbox_%s_results.json' % (test_data, test_data))
det_data = load_json_file(val_res_file)
det_data = group_bboxs(det_data)
gt_data = group_bboxs(gt_data['annotations'])
judged_det = judge_detection_results(det_data, gt_data)

det_data = load_json_file(test_res_file)
det_data = group_bboxs(det_data)
judged_det2 = judge_detection_results(det_data, None)

roc = generate_roc(judged_det, judged_det2)
with open(os.path.join(output_root, model_name, 'pn_curve.txt'), 'wt') as fp:
    for line in roc:
        fp.write('%f %f %f\n' % line)
print 'saved pn_curve.'

print get_threshold_by_false_rate(roc, 0.0312)
print get_threshold_by_false_rate(roc, 0.074)
print get_threshold_by_false_rate(roc, 0.059)
print get_threshold_by_false_rate(roc, 0.0913)
