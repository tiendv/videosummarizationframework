import numpy as np
from cpd_nonlin import cpd_nonlin
from cpd_auto import cpd_auto

class KTS:
    def __init__(self,feature):
        """ init function

        Arguments:
            feature {numpy.ndarray} -- array feature

        Writer: 
            thinhplg - 27/04/2020
        """        
        self.kernel = np.dot(feature, feature.T)

    def _auto(self,vmax=1,ncp=5):
        """[KTS auto choose number change points]

        Keyword Arguments:
            vmax {int} -- [Parameter for KTS, lower value means more clips] (default: {1})
            ncp {int} -- [Number change point (optinal)] (default: {5})
        Returns:
            [shot] -- [Array of detected change point]
            [score] -- [Array of costs for 0,1,2,...,ncp change-points]

        Writer:
            thinhplg - 27/04/2020
        """

        shot,score = cpd_auto(self.kernel,ncp, vmax)

        return shot,score
    
    def kts_nonlin(self,ncp,lmin=1,lmax=1000000):
        """[KTS change point detection]

        Arguments:
            ncp {int} -- [Number change point (required parameters)]
            lmin {int} -- [minimal length of a segment] (default: {1})
            lmax {int}]} -- [maximal length of a segment]

        Returns:
            [shot] -- [Array of detected change point]
            [score] -- [Array of costs for 0,1,2,...,ncp change-points]

        """
        shot, scores = cpd_nonlin(self.kernel, ncp, lmin, lax)
        return shot,scores 