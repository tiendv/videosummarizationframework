import random
def random_score(list_begin):
    '''
        This function generates the score for each shot randomly
        input: list_begin - list of the begin time of each shots
               list_ending - list of the end time of each shots
        output: a score list of shots.
    '''
    list_score = []
    for _ in range(len(list_begin)):
        list_score.append(round(random.randint(10,50)/10,1))
    return list_score
