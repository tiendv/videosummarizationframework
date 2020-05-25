import numpy as np
import sys
sys.path.append('/mmlabstorage/workingspace/VideoSum/videosummarizationframework/libs/KTS-kernel-temporal-segmentation')
from cpd_nonlin import cpd_nonlin
from cpd_auto import cpd_auto

def _output(typeout,shot,length_feture):
    if typeout == 0:
        return shot
    elif typeout == 1:
        change_points = np.concatenate(([0], shot, [length_feture-1]))
        return change_points
    elif typeout == 2:
        change_points = np.concatenate(([0], shot, [length_feture-1]))
        temp_change_points = []
        for idx in range(len(change_points)-1):
            segment = [change_points[idx], change_points[idx+1]]
            if idx == len(change_points)-2:
                segment = [change_points[idx], change_points[idx+1]]

            temp_change_points.append(segment)
        change_points = np.array(list(temp_change_points))
        return change_points
    elif typeout == 3:
        change_points = np.concatenate(([0], shot, [length_feture-1]))
        temp_change_points = []
        for idx in range(len(change_points)-1):
            segment = [change_points[idx], change_points[idx+1]-1]
            if idx == len(change_points)-2:
                segment = [change_points[idx], change_points[idx+1]]

            temp_change_points.append(segment)
        change_points = np.array(list(temp_change_points))
        return change_points
    
def KTS_auto(feature,max_ncp,vmax=1,type_output=1):
    """KTS auto
     Detect change points automatically selecting their number

    Arguments:
        feature {array 1D or 2D} -- Feature of data
        max_ncp {int} -- maximum number of change points to detect (ncp >= 0)

    Keyword Arguments:
        vmax {int} -- parameter for kts (default: {1})
        type_output {int} -- Type of output (default: {1})

    Returns:
        Change Points -- Results of KTS
    """    
    kernel = np.dot(feature, feature.T) #make kernel. Kernel between each pair of frames in video
    shot,_ = cpd_auto(kernel,max_ncp, vmax) #get change points (shot), and score of it (_)
    if type_output>3 or type_output<0:  #Check type of output result
        print("Error: Type of output results must be equal [0,1,2,3]")
        sys.exit()
    return _output(type_output,shot,len(feature))
    

def KTS_nonlin(feature,ncp,lmin,lmax,vmax=1,type_output=1):
    """KTS

    Arguments:
        feature {array 1D or 2D} -- Feature of data
        ncp {int} -- number of change points to detect (ncp >= 0)
        lmin {int} -- minimal length of a segment
        lmax {int} -- maximal length of a segment
    ncp - number of change points to detect (ncp >= 0)
    Keyword Arguments:
        vmax {int} -- [description] (default: {1})
        type_output {int} -- [description] (default: {1})

    Returns:
        [type] -- [description]
    """    
    kernel = np.dot(feature, feature.T)
    shot,_ = cpd_nonlin(kernel,ncp,lmin,lmax)    #Change point detection with dynamic programming
    if type_output>3 or type_output<0:
        print("Error: Type of output results must be equal [0,1,2,3]")
        sys.exit()
    return _output(type_output,shot,len(feature))