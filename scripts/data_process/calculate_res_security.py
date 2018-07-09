import json
import os
import sys
from eval_funs import *


def load_json_file(json_file):
    with open(json_file, 'rt') as fp:
        return json.load(fp)

def get_res_folder(model):
    model_map = {
         'sr1': 'security_r1_e2e_faster_rcnn_R-101-FPN_1x.yaml',
         's1': 'security1_e2e_faster_rcnn_R-101-FPN_1x.yaml',
         's1a': 'security1a_e2e_faster_rcnn_R-101-FPN_1x.yaml',         
         's2': 'security2_e2e_faster_rcnn_R-101-FPN_1x.yaml',         
         's2p': 'security2p_e2e_faster_rcnn_R-101-FPN_1x.yaml',             
         's3': 'security3_e2e_faster_rcnn_R-101-FPN_1x.yaml',
         's3_rpnfg0.4': 'security3_e2e_faster_rcnn_R-101-FPN_rpnfg0.4_1x.yaml',
         's3_rpnfg0.3': 'security3_e2e_faster_rcnn_R-101-FPN_rpnfg0.3_1x.yaml',            
         's3_rpnfg0.2': 'security3_e2e_faster_rcnn_R-101-FPN_rpnfg0.2_1x.yaml',                                          
         's3_fg0.05': 'security3_e2e_faster_rcnn_R-101-FPN_fg0.05_1x.yaml',   
         's3_fg0.005': 'security3_e2e_faster_rcnn_R-101-FPN_fg0.005_1x.yaml',         
         's3_fg0.01': 'security3_e2e_faster_rcnn_R-101-FPN_fg0.01_1x.yaml',                       
         's3_fg0.1': 'security3_e2e_faster_rcnn_R-101-FPN_fg0.1_1x.yaml',
         's3_bgl0.1': 'security3_e2e_faster_rcnn_R-101-FPN_bgl0.1_1x.yaml',                  
	     's4': 'security4_e2e_faster_rcnn_R-101-FPN_1x.yaml',
	     's7': 'security7_e2e_faster_rcnn_R-101-FPN_1x.yaml',
	     's3_ms': 'security3_e2e_faster_rcnn_R-101-FPN_ms_1x.yaml',
	     's4_ms': 'security3_e2e_faster_rcnn_R-101-FPN_ms_1x.yaml',
	     'r1': 'security1_retinanet_R-101-FPN_1x.yaml',
	     'rr1': 'security_r1_retinanet_R-101-FPN_1x.yaml',
	     'rr1m': 'security_r1m_retinanet_R-101-FPN_1x.yaml',	     
	     'r1a': 'security1a_retinanet_R-101-FPN_1x.yaml',		 		 		 
	     'r2': 'security2_retinanet_R-101-FPN_1x.yaml',
	     'r2p': 'security2_retinanet_R-101-FPN_1x.yaml',		 
	     'r3': 'security3_retinanet_R-101-FPN_1x.yaml',
	     'r4': 'security4_retinanet_R-101-FPN_1x.yaml'}

    if model not in model_map.keys():
        print 'None-Supported model %s' % model
        raise

    return model_map[model]
    
# plot_roc
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage:"
        print '\tpython %s model' % (__file__)
        print '\t-- model: security7 security4 security4_ms security3 or security3_ms'
        sys.exit(0)

output_root = '/home/amax/workspace/Detectron/detectron-output'
# val_data = 'security_train_real_package_val'
# test_data = 'security_train_real_package_val'
val_data = 'security_val_real_package'
test_data = 'security_val_real_package'
model_name =  get_res_folder(sys.argv[1])
# gt_data = load_json_file('/home/amax/data/securityData/annotations/instances_train_Real-Package_val.json')
gt_data = load_json_file('/home/amax/data/securityData/annotations/instances_val_Real-Package.json')
if sys.argv[1][0] == 's':
    val_res_file = os.path.join(output_root, model_name, 'test/test/%s/generalized_rcnn/bbox_%s_results.json' % (val_data, val_data))
    if os.path.exists(val_res_file):
        test_res_file = os.path.join(output_root, model_name, 'test/test/%s/generalized_rcnn/bbox_%s_results.json' % (test_data, test_data))
    else:
        val_res_file = os.path.join(output_root, model_name, 'test/%s/generalized_rcnn/bbox_%s_results.json' % (val_data, val_data))    
        test_res_file = os.path.join(output_root, model_name, 'test/%s/generalized_rcnn/bbox_%s_results.json' % (test_data, test_data))
        
elif sys.argv[1][0] == 'r':
    val_res_file = os.path.join(output_root, model_name, 'test/%s/retinanet/bbox_%s_results.json' % (val_data, val_data))
    test_res_file = os.path.join(output_root, model_name, 'test/%s/retinanet/bbox_%s_results.json' % (test_data, test_data))
else:
    print 'None-Supported model %s' % sys.argv[1]
    raise
    
det_data = load_json_file(val_res_file)
det_data = group_bboxs(det_data)
gt_data = group_bboxs(gt_data['annotations'])
judged_det, gt_num, ins_num = judge_detection_instances(det_data, gt_data)

categories = ['knife', 'gun']
roc = generate_instance_roc(judged_det, gt_num, ins_num)
# print roc
false_rates = [0.001, 0.005, 0.01, 0.03, 0.05, 0.1]
hit_rates = [0.995, 0.99, 0.98, 0.95, 0.9]
heads = ['False Rate', 'Detection Rate', 'Score']
print '-------------------------------------------'
print '%s' % '\t'.join(heads)
for fr in false_rates:
    tmp = get_threshold_by_false_rate(roc, fr)
    print '%.2f\t%.2f\t%.4f' %(fr*100, tmp[0]*100, tmp[2])
print '-------------------------------------------'
# print roc    
for hr in hit_rates:
    tmp = get_threshold_by_hit_rate(roc, hr)
    print '%.2f\t%.2f\t%.4f' %(tmp[1]*100, tmp[0]*100, tmp[2])    
print '-------------------------------------------'
# roc = generate_roc(judged_det, judged_det2)
# with open(os.path.join(output_root, model_name, 'pn_curve.txt'), 'wt') as fp:
#     for line in roc:
#         fp.write('%f %f %f\n' % line)
# print 'saved pn_curve.'

# print '##########Thres by false rate #############'
# print get_threshold_by_false_rate(roc, 0.01)
# print get_threshold_by_false_rate(roc, 0.0312)
# print get_threshold_by_false_rate(roc, 0.059)
# print get_threshold_by_false_rate(roc, 0.074)
# print get_threshold_by_false_rate(roc, 0.0913)
# print '###########Thres by hit rate  #############'
# print get_threshold_by_hit_rate(roc, 0.8)
# print get_threshold_by_hit_rate(roc, 0.9)
# print get_threshold_by_hit_rate(roc, 0.95)
# print get_threshold_by_hit_rate(roc, 0.98)
# print get_threshold_by_hit_rate(roc, 0.99)

