import sys, os
import gm_submodular
import gm_submodular.example_objectives as ex
from gm_submodular import leskovec_maximize


from func.dataset.summe_events import SUMME
import numpy as np
import scipy.spatial.distance as dist


class VSUM(gm_submodular.DataElement):

    def __init__(self, videoID, model,fps,duration,path_npy,total_frames,path_reference,
                 dataset='summe',
                 seg_l=5):
        # load dataset data
        self.dataset = SUMME(videoID,fps,duration,path_npy,total_frames,path_reference)

        # budget 15% of orig
        self.budget = int(0.15 * self.dataset.data['length'] / seg_l)
        #print 'budget: ', self.budget

        # embed video segments
        seg_feat = encodeSeg(self.dataset, model, seg_size=seg_l)

        # store segment features
        self.x = seg_feat
        self.Y = np.ones(self.x.shape[0])

        # compute distance between segments
        self.dist_e = dist.squareform(dist.pdist(self.x, 'sqeuclidean'))

        # compute chronological distance
        self.frame, img_id, self.score = self.dataset.sampleFrame()

#        print(len(self.score))
        fno_arr = np.expand_dims(np.array(img_id), axis=1)
        self.dist_c = dist.pdist(fno_arr, 'sqeuclidean')

    def getCosts(self):
        return np.ones(self.x.shape[0])

    # def getRelevance(self):
    #     return np.multiply(self.rel, self.rel)

    def getChrDistances(self):
        d = dist.squareform(self.dist_c)
        return np.multiply(d, d)

    def getDistances(self):
        return np.multiply(self.dist_e, self.dist_e)

    def summarizeRep(self, weights=[1.0, 0.0], seg_l=5):

        objectives = [representativeness(self),
                      uniformity(self)]

        selected, score, minoux_bound = leskovec_maximize(self,
                                                          weights,
                                                          objectives,
                                                          budget=self.budget)

        selected.sort()

        frames = []
        gt_score = []
        for i in selected:
            frames.append(self.frame[i:i + seg_l])
            print self.frame[i:i + seg_l]
            gt_score.append(self.score[i:i + seg_l])

        return selected, frames, gt_score


def encodeSeg(data, model, seg_size=5):
    feat_temp = data.feat     #shape : fnum
    feat = []
    print feat_temp.shape
    for i in range(feat_temp.shape[0]-seg_size):
        temp = []
        for j in range(feat_temp.shape[1]):
            total = 0
            for k in range(seg_size):
                total += feat_temp[i+k][j]
            total=total/seg_size
            temp.append(total)
        feat.append(temp)
    feat=np.array(feat)

    return feat

################################################
# objectives
################################################
def uniformity(S):
    '''
    Based on representativeness_shell implementation in 'example_objectives.py'
    :input S: DataElement with function getChrDistances()
    :return: uniformity objective
    '''
    tempDMat = S.getChrDistances()
    norm = tempDMat.mean()
    return (lambda X: (1 - ex.kmedoid_loss(X, tempDMat, float(norm))))


def representativeness(S):
    '''
    Based on representativeness_shell implementation in 'example_objectives.py'
    :input S: DataElement with function getDistances()
    :return: representativeness objective
    '''
    tempDMat = S.getDistances()
    norm = tempDMat.mean()
    return (lambda X: (1 - ex.kmedoid_loss(X, tempDMat, float(norm))))
