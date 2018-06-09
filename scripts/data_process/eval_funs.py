MAX_IMAGE_NUM = 100000

# -------------------------------------
# calculate IOU of two rects
#     input: r1, r2 ~ (x, y, w, h)
#     output: iou
def calc_iou(r1, r2):
    ox1 = max(r1[0], r2[0])
    oy1 = max(r1[1], r2[1])
    ox2 = min(r1[0]+r1[2], r2[0]+r2[2])
    oy2 = min(r1[1]+r1[3], r2[1]+r2[3])
    oa = (ox2 - ox1)*(oy2 - oy1)
    return oa*1.0/(r1[2]*r1[3]+r2[2]*r2[3] - oa)

# -------------------------------------
# group the detection results, according to their image_id
# image_ids is assumed smaller than MAX_IMAGE_NUM
#     input: list of objects, each object is a dict contains 'image_id', 'category_id', 'bbox', 'score'
#     output: list of list of objects, number of sublists is equal to number of images (empty sublist may exist)
def group_bboxs(obj_list):    
    im_num = 0
    im_bboxs = [list() for i in range(MAX_IMAGE_NUM)]
    for obj in obj_list:
        im_bboxs[obj['image_id']].append(obj)
        im_num = max(im_num, obj['image_id'])
    return im_bboxs[:im_num + 1]



def judge_detection_instances(dets, gt, iou=0.5):    
    res = []    
    print '%d dets to be judge' % len(dets)
    gt_num = 0
    ins_num = 0
    for im_idx, im_det in enumerate(dets):
        # find all unmatched detections
        gt_num += len(gt[im_idx])
        ins_num += len(im_det)
        for (oi, obj) in enumerate(im_det):
            max_score = 0
            for gt_obj in gt[im_idx]:
                if obj['category_id'] == gt_obj['category_id'] and calc_iou(obj['bbox'], gt_obj['bbox']) >= iou:
                    max_score = obj['score']
                    break                                
            # no matched ground truth
            if max_score == 0:
                judge = (0, obj['score'], obj['category_id'])
                im_det.pop(oi)        
            res.append(judge) 
        # find all matched detections with ground truth
        for gt_obj in gt[im_idx]:
            max_score = 0
            for (oi, obj) in enumerate(im_det):
                if obj['category_id'] == gt_obj['category_id'] and calc_iou(obj['bbox'], gt_obj['bbox']) >= iou:
                    max_score = max(max_score, obj['score'])                    
            # Note, one detection is allowed to match multiple gts
            # Need to check COCO AP
            if max_score != 0:
                judge = (1, max_score, obj['category_id'])                 
            res.append(judge)                 
    # detection rate = sum(judge == 1) / gt_num
    # false det rate = sum(judge == 0) / len(dets)
    return res, gt_num, ins_num



# -------------------------------------
# judge a list, number of images, is correct or not, with score
#     input: list of list of objects, retruned by group_bboxs
#     output: judge results, each element is a pair (0/1, score). 0/1 means if the image is kongbao or not.
def judge_detection_images(dets, gt=None, iou=0.5):
    is_kongbao = (gt is None)
    
    res = []    
    print '%d dets to be judge' % len(dets)
    for im_idx, im_det in enumerate(dets):
        if is_kongbao:            
            max_score = 0
            for obj in im_det:
                max_score = max(max_score, obj['score'])
            judge = (0, max_score, obj['category_id']) # correctness, score, cate
            res.append(judge) 
        else:
            # normal image, find the max_score for corrected ones.            
            # How to determine an image is correct or not
            
            # 1. Any contraband object is detected                        
#            for obj1 in im_det:
#                max_score = max(max_score, obj1['score'])                        
            
            # 2. At least one object is correctly detected
#             max_score = 0
#             for obj1 in im_det:
#                 for obj2 in gt[im_idx]:
#                     if obj1['category_id'] == obj2['category_id'] and calc_iou(obj1['bbox'], obj2['bbox']) >= iou:
#                         max_score = max(max_score, obj1['score'])                        
#             judge = (1, max_score)
            # 3. judge each instance
            for obj1 in im_det:
                max_score = 0
                for obj2 in gt[im_idx]:
                    if obj1['category_id'] == obj2['category_id'] and calc_iou(obj1['bbox'], obj2['bbox']) >= iou:
                        max_score = obj1['score']
                        break
                        #max_score = max(max_score, obj1['score'])                        
                # no matched ground truth
                if max_score == 0:
                    judge = (0, obj1['score'], obj1['category_id'])
                else:
                    judge = (1, obj1['score'], obj1['category_id'])
                res.append(judge)             

    return res

# -------------------------------------
# generate roc curve
#     input: judged_detection results, 
#     output: list of (hit rate, false rate, threshold)
def generate_instance_roc(dets, gt_num, ins_num):    
    dets.sort(key=lambda x: -x[1])
#    print dets
#     fg_num = 0
#     bg_num = 0
#     roc = []
#     for x in dets:
#         if x[0] == 0:
#             bg_num += 1
#         else:
#             fg_num += 1
    fg_count = 0
    bg_count = 0
    roc = []
    for x in dets:
        if x[0] == 0:
            bg_count += 1
        else:
            fg_count += 1
        roc.append((fg_count*1.0/gt_num, bg_count*1.0/ins_num, x[1]))
    return roc


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
    print 'In total %d WJP, and %d KB' % (wjp_num, kb_num)
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

# -------------------------------------
#
def get_threshold_by_false_rate(roc, fr):
    for (idx, item) in enumerate(roc):
        if item[1] > fr:
            return roc[idx-1]
    return roc[-1]

# -------------------------------------    
def get_threshold_by_hit_rate(roc, hr):
    for (idx, item) in enumerate(roc):
        if item[0] > hr:
            return roc[idx]
    return roc[-1]    

