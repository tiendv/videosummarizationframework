import random
import numpy as np
def random_score(nFrames):
    '''
        This function generates the score for each shot randomly
        input: nFrames - #frames or #shots

        output: a score array.
    '''
    rand_score = np.random.random((nFrames,))
    return rand_score
