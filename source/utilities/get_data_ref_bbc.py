from .config.config import cfg
def get_data_ref_bbc(path_ref_bbc):
    '''
        This function will return the information about video id, and time of each shot in BBC dataset
        input: path_ref_bbc - the path of the master processed of bbc file
        output: ret - a dictionary with the key and value is the video_id and video_name, respectively
                dict_time - a dictionary with the key and value is the shot_id and its time, respectively
    '''
    ret = dict()
    dict_time = dict()
    with open(path_ref_bbc, 'r') as f:
        for line in f:
            video_name, shot_id, st, ed = line.rstrip().split()
            video_name = video_name.split('.')[0]
            video_id = shot_id.split('_')[0][4:]
            ret[video_id] = video_name
            dict_time[shot_id] = [st,ed]
    return ret,dict_time

if __name__ == '__main__':
    ref_id, time_shots = get_data_ref_bbc(cfg.PATH_DATA_REF_BBC_FILE)
    print(time_shots['shot62.1975'])

