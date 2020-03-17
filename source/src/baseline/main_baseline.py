import argparse
from segmentation.create_json_from_time_shots import create_json4shots
from selection.get_data_to_selection import create_json_selection_file,selection_shot_knapsack_file,get_data_to_selection,selection_shot_knapsack, create_json_selection

def main_baseline(path_video,path_saved_json_shot="./",path_saved_json_segment='./'):
    '''
        This function uses to summarize a video and export json files for visualization
        input: path_save - path of a input video_duration
               path_saved_json_shot - path to save json file for visualizing shots
               path_saved_json_segment -  path to save json file for visualizing segments
        output: None
    '''
    #shot detection
    name_video,list_begin, list_ending = split_shots(path_video)

    #cacl score
    list_score = calc_score(list_begin,list_ending)

    #create json to visual shots
    create_json4shots(path_saved_json_shot,name_video,list_begin,list_ending,list_score,"shot_bl")

    #excuting knapsack to select the shots for summarize
    result = selection_shot_knapsack(list_begin,list_ending,list_score)

    create_json_selection(name_video,list_begin,list_ending,result,path_saved_json_segment,"seg_bl")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optional description')
    parser.add_argument('path_video', type=str,
                    help='path of a input video')
    parser.add_argument('--path_shot', type=str,
                    help='path to save json file for visualizing shots')
    parser.add_argument('--path_seg', type=str,
                    help='path to save json file for visualizing segs')
    args = parser.parse_args()
    main_baseline(args.path_video)
