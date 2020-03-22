def get_data_ref_bbc(path_ref_bbc):
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
