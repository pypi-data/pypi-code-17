# tools for retrieval related processing


import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import json

class DistType:
    Hamming = 0,
    L2 = 1

class ReduceType:
    MeanMin = 0,
    Min = 1

# inputs have to be matrix, output is row(query_codes) x row(db_codes) distmat
def comp_distmat(query_feats, db_feats, dist_type=DistType.Hamming):
    if dist_type==DistType.L2:
        # l2 normalization
        from numpy import linalg as LA
        import numpy.matlib
        qnorm = LA.norm(query_feats, axis=1)
        query_feats = np.divide(query_feats, np.tile(qnorm,(query_feats.shape[1],1)).T)
        if db_feats is not None:
            dbnorm = LA.norm(db_feats, axis=1)
            db_feats = np.divide(db_feats,np.tile(dbnorm,(db_feats.shape[1],1)).T)
    print('start matching...')
    if db_feats is None:
        db_feats = query_feats
    if dist_type == DistType.Hamming:
        dist_mat = scipy.spatial.distance.cdist(query_feats, db_feats, 'hamming')
    if dist_type == DistType.L2:
        dist_mat = scipy.spatial.distance.cdist(query_feats, db_feats, 'euclidean')

    print('search done. distance matrix shape: {}'.format(dist_mat.shape))
    return dist_mat

# return a reduced distance matrix with a single value for
def reduce_distmat(full_dist_mat, gal_templateids, probe_templateids, reduce_type=ReduceType.MeanMin):
    # Get unique template indices and there positions for keeping initial order
    #gal_tuids,gal_tuind=np.unique(gal_templateids,return_index=True)
    #probe_tuids,probe_tuind=np.unique(probe_templateids,return_index=True)
    gal_tuids,gal_tuind=np.unique([str(x) for x in gal_templateids],return_index=True)
    probe_tuids,probe_tuind=np.unique([str(x) for x in probe_templateids],return_index=True)
    red_dist_mat = np.zeros((len(gal_tuids),len(probe_tuids)))
    # Loop on gallery
    for g,gtupos in enumerate(gal_tuind):
        gutid = gal_templateids[gtupos]
        gt_pos = np.where(gal_templateids==gutid)[0]
        # Loop on probe
        for p,ptupos in enumerate(probe_tuind):
            putid = probe_templateids[ptupos]
            pt_pos = np.where(probe_templateids==putid)[0]
            # Get appropriate distance
            #print g,p
            dist_val = 0.0
            # TO BE FIXED
            if reduce_type==ReduceType.MeanMin:
                dist_val = np.mean(np.min(full_dist_mat[np.ix_(gt_pos,pt_pos)]))
            else:
                dist_val = np.amin(full_dist_mat[np.ix_(gt_pos,pt_pos)])
            red_dist_mat[g,p]=dist_val
    return red_dist_mat,gal_tuind,probe_tuind



class PtSetDist():
    Min = 0,
    Avg = 1,
    MeanMin = 2 # TO BE IMPLEMENTED

# compute distance between set pairs using point
# min point pair or avg point pair, distance matrix: query -> db
# input codes are list of tensors
def match_set_with_pts(db_set_feats, query_set_feats, dist_type, pt_set_dist_mode):
    print('start matching sets using points...')
    dist_mat = np.empty((len(query_set_feats), len(db_set_feats)), dtype=np.float)
    for i in range(len(query_set_feats)):
        for j in range(len(db_set_feats)):
            if dist_type == DistType.Hamming:
                tmp_dist_mat = scipy.spatial.distance.cdist(query_set_feats[i], db_set_feats[j], 'hamming')
            if dist_type == DistType.L2:
                tmp_dist_mat = scipy.spatial.distance.cdist(query_set_feats[i], db_set_feats[j], 'euclidean')
            if pt_set_dist_mode == PtSetDist.Min:
                dist_mat[i,j] = np.amin(tmp_dist_mat)
            if pt_set_dist_mode == PtSetDist.Avg:
                dist_mat[i,j] = np.mean(tmp_dist_mat)
            if pt_set_dist_mode == PtSetDist.MeanMin:
                dist_mat[i,j] = np.mean(np.amin(tmp_dist_mat, axis=1))
    return dist_mat


# draw one or more pr curves in a plot
# pr curve format: {'name', 'pre', 'recall', 'map'}
def draw_pr_curves(plot_title, pr_curves, save_fn=''):
    plt.figure()
    symbols = ['.', 'o', 'x', '+', 'd', 'v', '>', 's', 'p', '*', 'h']
    for i in range(len(pr_curves)):
        precision = pr_curves[i]['pre']
        recall = pr_curves[i]['recall']
        plt.plot(recall.tolist(), precision.tolist(), symbols[i]+'-', label=pr_curves[i]['name'])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(plot_title)
    plt.xlim([0, 1])
    plt.ylim([0, 1.1])
    plt.legend(loc=4, fontsize=10)
    plt.grid()
    if save_fn != '':
        plt.savefig(save_fn)

# compute multiple performance metrics
# pr curve, map, classification accu using NN
def evaluate(plot_title, dist_mat, db_labels, query_labels, save_fn_prefix=''):
    print 'start evaluation'
    top1 = float(0)
    top5 = float(0)
    rank_num = 100
    precision = np.zeros(rank_num)
    recall = np.zeros(rank_num)
    map = 0
    valid_query_num = 0
    clf_accu_nn = 0
    # check each query
    for id in range(len(query_labels)):
        sorted_db_ids = np.argsort(dist_mat[id,:])
        sorted_db_labels = [db_labels[i] for i in sorted_db_ids]
        sorted_label_mask = sorted_db_labels == query_labels[id]
        clf_accu_nn += int(sorted_label_mask[0])
        total_cnt = sorted_label_mask.sum()
        # ignore nonexisting probe label
        if total_cnt == 0:
            continue
        cnt = 0
        cur_precision = np.zeros(rank_num)
        cur_recall = np.zeros(rank_num)
        for k in np.linspace(start=0, stop=len(db_labels), num=rank_num):
            corr = sorted_label_mask[0:k+1].sum() * 1.0
            recall[cnt] += corr / total_cnt
            cur_recall[cnt] += corr / total_cnt
            precision[cnt] += corr / (k+1)
            if cnt == 0:
                cur_precision[cnt] = (corr / (k+1)) * cur_recall[cnt]
            else:
                cur_precision[cnt] = (corr / (k+1)) * (cur_recall[cnt]-cur_recall[cnt-1])
            cnt += 1
        map += np.sum(cur_precision)
        if id % len(query_labels)/100 == 0:
            print('finished {}'.format(id))
        valid_query_num += 1

    map /= valid_query_num
    print('MAP: {}'.format(map))
    clf_accu_nn = clf_accu_nn * 1.0 / valid_query_num
    print 'classification accuracy: {}'.format(clf_accu_nn)

    precision /= valid_query_num
    recall /= valid_query_num
    pr_res = {}
    pr_res['name'] = plot_title
    pr_res['pre'] = precision
    pr_res['recall'] = recall
    pr_res['map'] = map
    pr_res['accu_nn'] = clf_accu_nn
    
    print precision
    print recall
    with open(save_fn_prefix + '.pr', 'w') as f:
        import copy
        pr_res_json = copy.deepcopy(pr_res)
        pr_res_json['pre'] = np.array_str(precision)
        pr_res_json['recall'] = np.array_str(recall)
        json.dump(pr_res_json, f)
        print 'pr curve saved to {}'.format(save_fn_prefix+'.pr')

    prs = [pr_res]
    draw_pr_curves(plot_title, prs, save_fn_prefix + '.png')
    

    #plt.show()
    #print('top1 accuracy: {:.3f}%, top5 accuracy: {:.3f}%'.format(top1*100, top5*100))
    #return top1, top5
